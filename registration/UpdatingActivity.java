package com.example.registration;

import static com.example.registration.R.id.btnupdate;
import static com.example.registration.R.id.imageButton4;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

public class UpdatingActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_updating);

        @SuppressLint("WrongViewCast") TextView btn=findViewById(btnupdate);
        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(UpdatingActivity.this,LibrarianActivity.class));
            }
        });
    }
}