from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment
 
 
env = StreamExecutionEnvironment.get_execution_environment().set_parallelism(1)
 
# Create a simple data source (a list of strings)
data = env.from_collection(
    collection=["Hello", "Flink", "Test"], type_info=Types.STRING()
)
 
# Print the elements to the console
data.print()
 
# Execute the Flink job
env.execute("Hello World")
 