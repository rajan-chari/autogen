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
using System;
using System.Collections.Generic;

namespace AutoGenCapCS
{
    public class RuntimeFactory : IRuntimeFactory
    {
        private readonly Dictionary<string, Func<IRuntime>> _runtimeCreators;

        public RuntimeFactory()
        {
            _runtimeCreators = new Dictionary<string, Func<IRuntime>>();

            // Register default runtime types
            RegisterRuntime("default", () => new Runtime());
            RegisterRuntime("zmq", () => new ZMQRuntime());
        }

        public void RegisterRuntime(string key, Func<IRuntime> creator)
        {
            if (!_runtimeCreators.ContainsKey(key))
            {
                _runtimeCreators[key] = creator;
            }
            else
            {
                throw new ArgumentException($"A runtime with the key '{key}' is already registered.");
            }
        }

        public IRuntime CreateRuntime(string key)
        {
            if (_runtimeCreators.TryGetValue(key, out var creator))
            {
                return creator();
            }
            else
            {
                throw new KeyNotFoundException($"No runtime registered with the key '{key}'.");
            }
        }
    }
}
