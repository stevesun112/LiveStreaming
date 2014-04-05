package com.javaorigin.rtpsender;

import android.app.AlertDialog;
import android.media.AudioManager;
import android.os.Bundle;
import android.os.StrictMode;
import android.app.Activity;
import android.content.Context;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class MainActivity extends Activity {

    private Button conButton;
    private Button extButton;
    private EditText IPAddressET;
    private EditText portET;
    private RTPStreamer rtpStreamer;

    @Override
	protected void onCreate(Bundle savedInstanceState) {

        final AudioManager audio =  (AudioManager) getSystemService(Context.AUDIO_SERVICE);
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
		StrictMode.setThreadPolicy(policy);

        //Get Components
        conButton = (Button)findViewById(R.id.ConnectButton);
        extButton = (Button)findViewById(R.id.ExtButton);
        IPAddressET = (EditText)findViewById(R.id.IPEditText);
        portET = (EditText)findViewById(R.id.PortEditText);


        //Listeners
        conButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                // Perform action on click

                String IPAddress = IPAddressET.getText().toString();
                String port = portET.getText().toString();

               //Start to stream
              try{
                  if(rtpStreamer == null){
                      rtpStreamer = new RTPStreamer();

                      rtpStreamer.Streaming(audio,IPAddress,port);
                      IPAddressET.setEnabled(false);
                      portET.setEnabled(false);
                      conButton.setEnabled(false);

                  }


              }catch(Exception e){
                  Log.e("----------------------", e.toString());
                  AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
                  builder.setMessage("Connection error! Please check your Internet connection");
                  builder.show();
                  e.printStackTrace();
              }
            }
        });

        extButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                // Perform action on click
               finish();

            }
        });
	}
}
