import traceback
import logging
import os
import pika
from pika.exchange_type import ExchangeType
import time
import random
from .connect import conn, cur
from .config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
from  ai_audio_models.SpeechRecognition import analyze_audio
from pprint import pprint
from vosk import Model
import boto3

def string_from_qid(qid):
  return f'question_id=CAST(\'{qid}\' as uuid)'

CP_S3_BUCKET_STRING = "https://coinplanet.s3.ap-south-1.amazonaws.com/"
SANITIZED_SAFE = "san_safe"
SANITIZED_UNSAFE = "san_unsafe"
SANITIZED_PENDING = "san_pending"
SANITIZATION_NOT_REQUESTED = "san_not_requested"

def on_message_received(ch, method, properties, body, model, s3_client):

    print("The body is ====> ", body)

    # convert byte string to string
    surveyId = body.decode('UTF-8')

    print(f'The surveyId is {surveyId}')

    cur.execute("SELECT * FROM public.\"Surveys\" WHERE id=CAST(%s as uuid);", (surveyId,))
    # select * from public."Surveys" where id=CAST('a9606715-c865-4f99-9afc-48b79af77caa' as uuid);

    survey = cur.fetchone()
    # survey is RealDictRow
    # get the "id", "form_title", "form_description" & "purpose"

    audio_list = [""]

    print("===== THE SURVEY AUDIO LIST ====")
    print(audio_list)

    if survey is not None:
      print("Survey exists ===>")

      cur.execute("SELECT * FROM public.\"Questions\" WHERE survey_id=CAST(%s as uuid);", (surveyId,))
      # SELECT * FROM public."Questions" WHERE survey_id=CAST('a9606715-c865-4f99-9afc-48b79af77caa' as uuid);

      questions = cur.fetchall()
      # get the "id", "title" & "description"

      question_ids = []

      if len(questions) > 0:
        for question in questions:
          
          question_ids.append(question['id'])

          audio_list.append(question['ques_audio'])

        query = f'SELECT * FROM public.\"Options\" WHERE ({" OR ".join(list(map(string_from_qid, question_ids)))})'

        cur.execute(query)
        # SELECT * FROM public."Options" WHERE (question_id=CAST('1b0fede5-b1ab-427e-9a98-d135c5c6a4db' as uuid) OR question_id=CAST('13fa4dcd-b514-483e-b699-ba9efb17a836' as uuid) OR question_id=CAST('7950a4b1-175f-466f-a826-81bf51dd781e' as uuid) OR question_id=CAST('f0ec6990-a71e-425b-8690-cc621f072293' as uuid) OR question_id=CAST('4a6d9b57-3bf1-4267-bedc-99537fd677ff' as uuid) OR question_id=CAST('2840ba65-a591-46c0-8558-908c823b4bd7' as uuid));

        all_options = cur.fetchall()

        if len(all_options) > 0:
          for option in all_options:
            audio_list.append(option['option_audio'])
        else:
          print("CONSUMER ERROR :- Cannot add survey to the Sanitization Queue bcz Question doesn't have any options")

        print("===== THE AUDIO LIST IS ======")

        print(audio_list, len(audio_list))

        data_sanitization_mapping = []

        # RUN THE ML CODE HERE
        for i in range(len(audio_list)):
            # analyzer = LR_analyze_data()
            if type(audio_list[i]) == str and CP_S3_BUCKET_STRING in audio_list[i]:
              data = analyze_audio(model, path=audio_list[i], beep=True)
              data_sanitization_mapping.append({
                  'audio_key' : audio_list[i],
                  'toxic': data["toxic"],
                  'dir_to_delete': data["dir_to_delete"],
                  'filename': data['filename'],
                  'extsn': data['extsn']
              })

        print("==========> The final result")
        pprint(data_sanitization_mapping)

        # const params = {
        #   Bucket: "coinplanet",
        #   Key: `users/${user.id}/forms/${surveyId}/`, // fileId & fileName will be added in the middleware
        #   ACL: "public-read",
        #   ContentType: "binary/octet-stream",
        # };

        # HARMFUL AUDIO
        toxic_audio_list = []
        for audio_dict in data_sanitization_mapping:
          harmful_list = {}
          if audio_dict["toxic"] == True:
            toxic_audio_list.append(audio_dict)
            try:
                new_audio_path = os.path.join(audio_dict["dir_to_delete"], audio_dict['filename'] + '.' + audio_dict['extsn'])
                s3_client.put_object(Bucket='coinplanet', Key=audio_dict["audio_key"].split(CP_S3_BUCKET_STRING)[1], ACL='public-read', ContentType= 'binary/octet-stream', Body=open(new_audio_path, 'rb'))
            except Exception as e:
                logging.error(traceback.format_exc())
                # Logs the error appropriately. 

        # upload the data to AWS & delete the temporary directories
        
        print("=======> The toxic_audio_list list is")
        pprint(toxic_audio_list)
        print("=======> len(toxic_audio_list)", len(toxic_audio_list))

        if len(toxic_audio_list) > 0:
          cur.execute("UPDATE public.\"Surveys\" SET sanitized_audio=%s WHERE id=CAST(%s as uuid);", (SANITIZED_UNSAFE, surveyId,))

          conn.commit()
        else :
          cur.execute("UPDATE public.\"Surveys\" SET sanitized_audio=%s WHERE id=CAST(%s as uuid);", (SANITIZED_SAFE, surveyId,))

          conn.commit()
      else:
        print("CONSUMER ERROR :- Cannot add survey to the Sanitization Queue bcz Survey doesn't hv any questions")

    else:
      print("CONSUMER ERROR :- Cannot add survey to the Sanitization Queue bcz survey doesn't exist")

    time.sleep(random.randint(2,4))

    # MANUALLY ACKNOWLEDGE AFTER PROCESSING IS COMPLETE
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("============= Finished processing audio data ===============")


def run_mq(consumer_name):
  # Changing Directory So That Processed Files & Folders Are Created In That Directory
  os.chdir('ai_audio_models')

  print("os.getcwd()", os.getcwd())

  print("===> Connecting to AWS")
  
  s3_client = boto3.client(service_name="s3", region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, 
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,)
  # bucket = s3_client.bucket('coinplanet')

  connection_parameters = pika.ConnectionParameters("localhost")

  connection = pika.BlockingConnection(connection_parameters)

  # We don't directly interact with Connections, we interact with Channels
  channel = connection.channel()

  AUDIO_QUEUE_NAME = "sanitize_survey_audio_queue"
  EXCHANGE_NAME = "cp_pub_sub_exchange"

  # We are declaring the exchange again bcz if we start the CONSUMER FIRST then the exchange will be created
  channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type=ExchangeType.fanout)

  # creating the queue :- IDEMPOTENT operation means it will be declared only once.
  channel.queue_declare(queue=AUDIO_QUEUE_NAME)

  # As discussed in README.md. Each Consumer will only process a single message at a time.
  # DEFAULT IS ROUND ROBIN
  channel.basic_qos(prefetch_count=1)

  channel.queue_bind(exchange=EXCHANGE_NAME, queue=AUDIO_QUEUE_NAME)

  print("===> Loading English-Indian Model")
        
  # Loading the model here to prevent loading the model again & again on func call. 
  # Also, model can be varied according to user's country
  model = Model(r'D:\D_Documents\AI_ML\vosk-models\vosk-model-en-in-0.5') 

  # REMOVED auto_ack :- Don't automatically acknowledge after consuming from the queue
  channel.basic_consume(
      queue=AUDIO_QUEUE_NAME, on_message_callback=lambda ch, method, properties, body: on_message_received(ch, method, properties, body, model, s3_client)
  )

  print(f"============== Audio Consumer '{consumer_name}' is up & running ==============")

  channel.start_consuming()