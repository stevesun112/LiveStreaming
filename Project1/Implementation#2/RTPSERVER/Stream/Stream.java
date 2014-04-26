package RTPSERVER.Stream;

import java.util.ArrayList;

/**
 * Created by christopherhuang on 4/2/14.
 */
public class Stream {
    public int ID;                     //integer marks the stream
    public int RTPPORT;                //port to receive packets from sender
    public MobileClient sender;         //mobile client collecting and sending the data
    public ArrayList<Viewer> viewers;   //list of viewers in the stream

    public Stream(int ID, int RTPPORT, MobileClient sender){
        this.ID = ID;
        this.RTPPORT = RTPPORT;
        this.sender = sender;
        this.viewers = new ArrayList<Viewer>();
    }
}
