using System;

namespace AutoGenCapCS
{
    public class Actor : IMsgActor
    {
        public void OnConnect() 
        { 
            Console.WriteLine("Connected."); 
        }

        public void OnTxtMsg(string message) 
        { 
            Console.WriteLine($"Text message received: {message}"); 
        }

        public void OnBinMsg(byte[] message) 
        { 
            Console.WriteLine($"Binary message received: {BitConverter.ToString(message)}"); 
        }

        public void DispatchMessage() 
        { 
            Console.WriteLine("Dispatching message."); 
        }

        public string GetMessage() 
        { 
            Console.WriteLine("Getting message.");
            return "Sample message"; 
        }

        public void OnStart() 
        { 
            Console.WriteLine("Actor started."); 
        }

        public void DisconnectNetwork() 
        { 
            Console.WriteLine("Network disconnected."); 
        }

        public void Stop() 
        { 
            Console.WriteLine("Actor stopped."); 
        }
    }
}
