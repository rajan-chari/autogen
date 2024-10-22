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
        public void SendTxtMsg(string message) { /* Implementation */ }
        public void SendBinMsg(byte[] message) { /* Implementation */ }
        public void SendProtoMsg(object protoMessage) { /* Implementation */ }
        public object SendRecvProtoMsg(object protoMessage) { /* Implementation */ return null; }
        public string SendRecvMsg(string message) { /* Implementation */ return ""; }
        public void Close() { /* Implementation */ }
    }
}
