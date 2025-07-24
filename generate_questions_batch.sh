#!/bin/bash

# Shell script to generate questions for Grade 10 topics
# Runs the question generator 50 times for each topic

# Array of topics
topics=(
    "Algebra"
    "Coordinate Geometry"
    "Functions"
    "Geometry"
    "Measurement and Applications"
    "Statistics and Probability"
    "Trigonometry"
)

# Array of complexities
complexities=(
    "easy"
    "medium"
    "hard"
)

# Configuration
GRADE=10
COUNT=5
RUNS_PER_TOPIC=50

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to log with timestamp
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

# Function to log success
log_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] ✓${NC} $1"
}

# Function to log warning
log_warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] ⚠${NC} $1"
}

# Function to log error
log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ✗${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "question-generator/question_generator.py" ]; then
    log_error "question_generator.py not found in question-generator directory"
    log_error "Please run this script from the Mathopedia root directory"
    exit 1
fi

# Change to question-generator directory
cd question-generator

log "Starting batch question generation for Grade $GRADE"
log "Topics: ${#topics[@]}"
log "Complexities: ${#complexities[@]}"
log "Runs per topic-complexity: $RUNS_PER_TOPIC"
log "Total runs: $((${#topics[@]} * ${#complexities[@]} * $RUNS_PER_TOPIC))"

# Track statistics
total_runs=0
successful_runs=0
failed_runs=0
start_time=$(date +%s)

# Loop through each topic
for topic in "${topics[@]}"; do
    log "Processing topic: $topic"
    
    # Loop through each complexity
    for complexity in "${complexities[@]}"; do
        log "  Processing complexity: $complexity"
        
        topic_complexity_start_time=$(date +%s)
        topic_complexity_successful=0
        topic_complexity_failed=0
        
        # Run the generator 50 times for each topic-complexity combination
        for i in $(seq 1 $RUNS_PER_TOPIC); do
            total_runs=$((total_runs + 1))
            
            log "    Run $i/$RUNS_PER_TOPIC for '$topic' - '$complexity'"
            
            # Run the question generator
            if python question_generator.py --grade $GRADE --topic "$topic" --complexity $complexity --count $COUNT --save; then
                successful_runs=$((successful_runs + 1))
                topic_complexity_successful=$((topic_complexity_successful + 1))
                log_success "      Completed run $i for '$topic' - '$complexity'"
            else
                failed_runs=$((failed_runs + 1))
                topic_complexity_failed=$((topic_complexity_failed + 1))
                log_error "      Failed run $i for '$topic' - '$complexity'"
            fi
            
            # Small delay to avoid overwhelming the system
            sleep 1
        done
        
        topic_complexity_end_time=$(date +%s)
        topic_complexity_duration=$((topic_complexity_end_time - topic_complexity_start_time))
        
        log_success "  Completed '$topic' - '$complexity': $topic_complexity_successful successful, $topic_complexity_failed failed (${topic_complexity_duration}s)"
    done
    
    log_success "Completed topic '$topic'"
    echo
done

# Calculate and display final statistics
end_time=$(date +%s)
total_duration=$((end_time - start_time))
hours=$((total_duration / 3600))
minutes=$(((total_duration % 3600) / 60))
seconds=$((total_duration % 60))

echo "=================================="
log_success "Batch generation completed!"
echo "=================================="
echo "Total runs: $total_runs"
echo "Successful: $successful_runs"
echo "Failed: $failed_runs"
echo "Success rate: $(echo "scale=2; $successful_runs * 100 / $total_runs" | bc -l)%"
echo "Total time: ${hours}h ${minutes}m ${seconds}s"
echo "Average time per run: $(echo "scale=2; $total_duration / $total_runs" | bc -l)s"
echo "=================================="

# Return to original directory
cd ..

# Exit with appropriate code
if [ $failed_runs -eq 0 ]; then
    log_success "All runs completed successfully!"
    exit 0
else
    log_warning "Some runs failed. Check the logs above for details."
    exit 1
fi
