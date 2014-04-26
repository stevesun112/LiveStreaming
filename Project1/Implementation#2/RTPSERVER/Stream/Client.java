package RTPSERVER.Stream;

import java.net.InetAddress;

/**
 * Created by christopherhuang on 4/2/14.
 */
public class Client {
    private InetAddress address;
    private int port;

    public Client(){
        this.address = null;
        this.port = 0;
    }

    public Client(InetAddress address, int port){
        this.address = address;
        this.port = port;
    }

    public InetAddress getAddress(){
        return this.address;
    }

    public void setAddress(InetAddress address){
        this.address = address;
    }

    public int getPort(){
        return this.port;
    }

    public void setPort(int port){
        this.port = port;
    }
}
