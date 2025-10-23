# GOOD: Multi-stage build for a TypeScript Node.js app

# Stage 1: Build environment
FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile
COPY . .
RUN yarn build # Compiles TypeScript to JavaScript

# Stage 2: Production environment
FROM node:20-alpine
WORKDIR /app
# Create a non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser
# Copy only necessary production artifacts
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package.json ./package.json # For production scripts if needed

# Expose port and define healthcheck
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl --fail http://localhost:3000/health || exit 1

CMD ["node", "dist/index.js"]
