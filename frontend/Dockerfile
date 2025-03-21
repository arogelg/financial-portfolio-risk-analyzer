# Use Node.js as base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package.json first to leverage Docker caching
COPY . .

# Install dependencies
RUN npm install

# Copy everything else
COPY . .

# Expose port 3000 for React
EXPOSE 3000

# Start the React app
CMD ["npm", "start"]