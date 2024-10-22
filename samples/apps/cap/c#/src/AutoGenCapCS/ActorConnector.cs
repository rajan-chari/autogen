namespace AutoGenCapCS
{
    public interface IActorConnector
    {
        void SendTxtMsg(string message);
        void SendBinMsg(byte[] message);
        void SendProtoMsg(object protoMessage);
        object SendRecvProtoMsg(object protoMessage);
        string SendRecvMsg(string message);
        void Close();
    }

    public class ActorConnector : IActorConnector
    {
        public void SendTxtMsg(string message) 
        { 
            // Send a text message
        }

        public void SendBinMsg(byte[] message) 
        { 
            // Send a binary message
        }

        public void SendProtoMsg(object protoMessage) 
        { 
            // Send a protocol message
        }

        public object SendRecvProtoMsg(object protoMessage) 
        { 
            // Send and receive a protocol message
            return null; 
        }

        public string SendRecvMsg(string message) 
        { 
            // Send and receive a text message
            return ""; 
        }

        public void Close() 
        { 
            // Close the connector
        }
    }
}
