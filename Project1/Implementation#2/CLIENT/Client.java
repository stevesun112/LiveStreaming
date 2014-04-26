package CLIENT;
/**
 * Created by christopherhuang on 3/24/14.
 */

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.net.Socket;

public class Client {
    public static void main(String[] args){
        String CLRF = "\r\n";
        String host = "localhost";
        int port = 22222;
        int LISTENINGPORT = 22222;
        Socket socket = null;

        System.out.println("Client is running");

        try{
            if (args.length == 3){
                host = args[0];
                port = Integer.parseInt(args[1]);
                LISTENINGPORT = Integer.parseInt(args[2]);
            }
            else{
                throw new Exception("Invalid Arguments");
            }
        }
        catch (Exception ex){
            System.out.println(ex);
            System.exit(0);
        }

        try{
            socket = new Socket(host, port);
            Writer writer = new BufferedWriter(new
                    OutputStreamWriter(socket.getOutputStream()));
            String request = "Add" + CLRF + LISTENINGPORT + CLRF;

            writer.write(request);
            writer.flush();
        }
        catch (IOException ex){
            System.out.print(ex);
        }
    }
}
