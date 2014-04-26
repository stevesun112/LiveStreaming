package RTPSERVER.Server;

import RTPSERVER.Stream.*;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;

/**
 * Created by christopherhuang on 3/27/14.
 * run the server in the command line
 * "java Server listeningport RTPport"
 */
public class Server {
    private int LISTENINGPORT;
    private int RTPPORT;
    private Stream stream;
    private final static String CLRF = "\r\n";

    public Server(int LISTENINGPORT, int RTPPORT){
        this.LISTENINGPORT = LISTENINGPORT;
        this.stream = new Stream(1, RTPPORT, new MobileClient());
    }

    /*
    run the server
     */
    public void run(){
        System.out.println("The server is running!");
        ServerSocket server = null;

        try {
            server = new ServerSocket(LISTENINGPORT);
            Thread thread = new Thread(new ForwardingRunnable(this.stream));

            thread.start();         //fork a thread to forward the RTP packet

            while (true){
                Socket connection = null;

                try{
                    connection = server.accept();
                    BufferedReader reader = new BufferedReader(
                            new InputStreamReader(connection.getInputStream()));
                    String request = reader.readLine();

                    System.out.println("Request:" + request);

                    if (request.equals("Add")){
                        int port = Integer.parseInt(reader.readLine());

                        //add a new viewer
                        synchronized (this.stream){
                            this.stream.viewers.add(
                                    new Viewer(connection.getInetAddress(), port));
                            printStream();
                        }
                    }
                }
                catch (IOException ex){
                    System.out.println(ex);
                }
            }
        }
        catch(IOException ex){
            System.out.print("Cannot Create Server!");
        }

    }

    public void printStream(){
        for (Viewer viewer : this.stream.viewers)
            System.out.println(viewer.getAddress().toString() + ":" + viewer.getPort());
    }

    public static void main(String[] args){
        Server server = null;

        try{
            if (args.length == 2){
                server = new Server(Integer.parseInt(args[0]), Integer.parseInt(args[1]));
            }
            else{
                throw new Exception("Invalid Arguments");
            }
        }
        catch (Exception ex){
            System.out.println(ex);
            System.exit(0);
        }

        server.run();
    }
}
