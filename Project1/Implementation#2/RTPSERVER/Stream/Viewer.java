package RTPSERVER.Stream;

import java.net.InetAddress;

/**
 * Created by christopherhuang on 4/2/14.
 */
public class Viewer extends Client{
    public Viewer(InetAddress address, int port){
        super(address, port);
    }
}
