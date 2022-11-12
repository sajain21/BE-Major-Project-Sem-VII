from audio_consumer import init_consumer
import sys

if __name__ == "__main__":

  if len(sys.argv) <= 1:
    exit("ERROR : Please give consumer name as an argument")
  else:
    # sys.argv[0] is the filename itself
    init_consumer(sys.argv[1])