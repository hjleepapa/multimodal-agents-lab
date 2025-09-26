#!/bin/bash

# Setup script for pushing to GitHub repository
# This script helps you create and push the multimodal-agents-lab to your GitHub account

echo "🚀 Setting up GitHub repository for Multimodal Agents Lab - Snowflake Edition"
echo ""

# Check if we're in the right directory
if [ ! -f "snowflake_solution_working_final.py" ]; then
    echo "❌ Error: Please run this script from the multimodal-agents-lab directory"
    exit 1
fi

echo "📋 Current Git status:"
git status --short

echo ""
echo "🔧 Current remote configuration:"
git remote -v

echo ""
echo "📝 To complete the setup, please follow these steps:"
echo ""
echo "1. 🌐 Go to GitHub and create a new repository:"
echo "   - Repository name: multimodal-agents-lab"
echo "   - Description: Multimodal AI agents solution with Snowflake integration"
echo "   - Make it public or private (your choice)"
echo "   - Don't initialize with README (we already have files)"
echo ""
echo "2. 🔑 Set up authentication (choose one):"
echo ""
echo "   Option A - Personal Access Token (Recommended):"
echo "   - Go to GitHub Settings > Developer settings > Personal access tokens"
echo "   - Generate a new token with 'repo' permissions"
echo "   - Run: git remote set-url origin https://YOUR_TOKEN@github.com/hjleepapa/multimodal-agents-lab.git"
echo ""
echo "   Option B - SSH Key:"
echo "   - Ensure your SSH key is added to GitHub"
echo "   - Run: git remote set-url origin git@github.com:hjleepapa/multimodal-agents-lab.git"
echo ""
echo "3. 🚀 Push the code:"
echo "   git push -u origin main"
echo ""
echo "4. ✅ Verify the repository:"
echo "   Visit: https://github.com/hjleepapa/multimodal-agents-lab"
echo ""

# Check if repository exists
echo "🔍 Checking if repository exists..."
if curl -s -o /dev/null -w "%{http_code}" https://github.com/hjleepapa/multimodal-agents-lab | grep -q "200"; then
    echo "✅ Repository already exists at https://github.com/hjleepapa/multimodal-agents-lab"
    echo "🚀 You can now push your code!"
    echo ""
    echo "To push immediately, run:"
    echo "git push -u origin main"
else
    echo "❌ Repository doesn't exist yet. Please create it on GitHub first."
    echo "🌐 Create repository: https://github.com/new"
    echo "📝 Repository name: multimodal-agents-lab"
fi

echo ""
echo "📚 After pushing, your repository will include:"
echo "   - Complete Snowflake multimodal agents solution"
echo "   - Comprehensive documentation"
echo "   - Test scripts and utilities"
echo "   - Migration guides"
echo "   - Working examples"
echo ""
echo "🎉 Happy coding!"
