
set -e  # Exit if any command fails

echo "Starting Flink JobManager..."
/docker-entrypoint.sh jobmanager &  # Start Flink JobManager in the background

echo "Submitting PyFlink jobs..."
for job in /opt/flink/jobs/*.py; do
    if [ -f "$job" ]; then
        echo "Submitting job: $job"
        flink run -m flink-jobmanager:8081 -py "$job"
        echo "Job submitted: $job"
    else
        echo "No Python jobs found in /opt/flink/jobs/"
    fi
done

echo "All jobs submitted!"

wait  # Keep the script running by waiting for background processes