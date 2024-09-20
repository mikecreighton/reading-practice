#!/bin/bash

# Function to send requests and capture the response
send_request() {
    local ip=$1
    curl -s -o /dev/null -w "%{http_code}" "http://localhost:8080/generate_story" \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        -H "X-Forwarded-For: $ip" \
        -d '{"words":"dog,cat,animal,bottle,tissue","subject":"Julian the waiter","setting":"A fancy restaurant","humor":"5","grade":"2nd"}'
}

# Function to simulate requests from different IPs
simulate_rate_limiting() {
    local num_requests=$1
    local ip_count=$2

    for ((i=0; i<num_requests; i++)); do
        # Generate a random IP address
        local ip=$((i % ip_count + 1))
        ip="192.168.1.${ip}"

        # Send the request
        (send_request $ip) &

        sleep 0.1
    done

    wait
}

# Number of requests to send
num_requests=20

# Number of unique IPs to simulate
ip_count=5

# Run the simulation
simulate_rate_limiting $num_requests $ip_count