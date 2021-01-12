FROM golang:1.13-alpine

RUN apk update && \
    apk upgrade && \
    apk add --no-cache bash git

RUN go get -u github.com/gin-gonic/gin
RUN go get -u github.com/jinzhu/gorm
RUN go get -u github.com/jinzhu/gorm/dialects/postgres

# Set the Current Working Directory inside the container
WORKDIR /go/src/airmon

# Copy everything from the current directory to the Working Directory inside the container
COPY . .

# Build the Go app
RUN go build -o main .

# Expose port 8081 to the outside world
EXPOSE 8081

# Run the executable DEPLOYMENT
CMD ./main