namespace AutoGenCapCS
{
    public interface IRuntimeFactory
    {
        IRuntime CreateRuntime();
        IRuntime CreateZMQRuntime();
    }

    public class RuntimeFactory : IRuntimeFactory
    {
        public IRuntime CreateRuntime()
        {
            // Default runtime creation logic
            return new Runtime();
        }

        public IRuntime CreateZMQRuntime()
        {
            // Create and return a new instance of ZMQRuntime
            return new ZMQRuntime();
        }
    }
}
