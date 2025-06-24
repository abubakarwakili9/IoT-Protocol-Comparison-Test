#!/bin/bash
# matter-project/build.sh

echo "🦀 Building Matter Protocol Analyzer with rs-matter..."

# Ensure we're in the matter-project directory
cd "$(dirname "$0")"

# Clean previous builds
echo "🧹 Cleaning previous builds..."
cargo clean

# Build the project
echo "🔨 Building rs-matter analyzer..."
cargo build --release

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo "📦 Binary location: target/release/matter_analyzer"
    echo "🚀 Run with: ./target/release/matter_analyzer"
else
    echo "❌ Build failed!"
    exit 1
fi