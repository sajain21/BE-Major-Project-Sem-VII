package com.example.registration;

import static com.example.registration.R.id.imageButton3;
import static com.example.registration.R.id.imageButton4;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

public class LibrarianActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_librarian);
        ImageView btn=findViewById(R.id.imageButton3);
        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(LibrarianActivity.this,DeleteActivity.class));
            }
        });

        ImageView btn2=findViewById(R.id.imageButton4);
        btn2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(LibrarianActivity.this,UpdatingActivity.class));
            }
        });

        ImageView btn3=findViewById(R.id.imageButton5);
        btn3.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(LibrarianActivity.this,ReturnBookActivity.class));
            }
        });
    }
}