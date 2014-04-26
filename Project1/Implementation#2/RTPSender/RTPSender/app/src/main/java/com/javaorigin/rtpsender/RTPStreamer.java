package com.javaorigin.rtpsender;

import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.NetworkInterface;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.util.Enumeration;

import android.app.AlertDialog;
import android.media.AudioManager;
import android.net.rtp.AudioCodec;
import android.net.rtp.AudioGroup;
import android.net.rtp.AudioStream;
import android.net.rtp.RtpStream;
import android.os.Bundle;
import android.os.StrictMode;
import android.app.Activity;
import android.content.Context;
import android.util.Log;
/**
 * Created by gynet on 4/2/14.
 */
public class RTPStreamer {

    private AudioStream audioStream;

    public void Streaming(AudioManager audio, String IPAddress, String port) throws Exception {
        try {
//            IPAddress = "134.84.218.34";
//            port = "22222";
            audio.setMode(AudioManager.MODE_IN_COMMUNICATION);
            AudioGroup audioGroup = new AudioGroup();
            audioGroup.setMode(AudioGroup.MODE_NORMAL);

            audioStream = new AudioStream(InetAddress.getByAddress(getLocalIPAddress ()));
            audioStream.setCodec(AudioCodec.PCMU);
            audioStream.setMode(RtpStream.MODE_NORMAL);
            audioStream.associate(InetAddress.getByName(IPAddress), Integer.parseInt(port)); //ipInetAddress.getByAddress(new byte[] {(byte)134, (byte)84, (byte)218, (byte)34}
            audioStream.join(audioGroup);


        } catch (Exception e) {
          throw e;
        }
    }
    public static byte[] getLocalIPAddress () {
        byte ip[]=null;
        try {
            for (Enumeration<NetworkInterface> en = NetworkInterface.getNetworkInterfaces(); en.hasMoreElements();) {
                NetworkInterface intf = en.nextElement();
                for (Enumeration<InetAddress> enumIpAddr = intf.getInetAddresses(); enumIpAddr.hasMoreElements();) {
                    InetAddress inetAddress = enumIpAddr.nextElement();
                    if (!inetAddress.isLoopbackAddress()) {
                        ip= inetAddress.getAddress();
                    }
                }
            }
        } catch (SocketException ex) {
            Log.i("SocketException ", ex.toString());
        }
        return ip;
    }


}
