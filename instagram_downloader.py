#!/usr/bin/env python
# Instagram Media Downloader
# This script downloads Instagram posts (images/videos) from specified profiles or post URLs

import instaloader
import os
import sys
import argparse
import re
from datetime import datetime
from getpass import getpass

def setup_argument_parser():
    """Set up command line argument parser"""
    parser = argparse.ArgumentParser(description='Download Instagram posts')
    parser.add_argument('-u', '--username', help='Your Instagram username (for private profile access)')
    parser.add_argument('-t', '--target', help='Target Instagram profile to download from')
    parser.add_argument('-c', '--count', type=int, default=0, help='Number of recent posts to download (0 for all)')
    parser.add_argument('-d', '--directory', default='downloads', help='Directory to save downloads')
    parser.add_argument('-p', '--posts-only', action='store_true', help='Download only posts (no stories, highlights, etc.)')
    parser.add_argument('-s', '--shortcode', help='Shortcode of a specific Instagram post to download')
    parser.add_argument('-P', '--post-url', help='URL of a specific Instagram post to download')
    parser.add_argument('--shortcodes-file', help='Path to a file containing shortcodes to download (one per line)')
    
    return parser

def create_instance(username=None):
    """Create and configure Instaloader instance"""
    L = instaloader.Instaloader(
        download_videos=True,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,  # Do not save JSON metadata files
        compress_json=False,
        post_metadata_txt_pattern=''
    )
    
    # Log in if username is provided
    if username:
        try:
            password = getpass(f"Enter password for {username}: ")
            L.login(username, password)
            print(f"Successfully logged in as {username}")
        except instaloader.exceptions.BadCredentialsException:
            print("Error: Invalid credentials")
            sys.exit(1)
        except instaloader.exceptions.ConnectionException:
            print("Error: Connection error during login")
            sys.exit(1)
            
    return L

def download_profile_posts(loader, target_profile, save_dir, count=0, posts_only=False):
    """Download posts from a target profile, saving each post in a folder named by its shortcode only (not inside downloads/)"""
    try:
        profile = instaloader.Profile.from_username(loader.context, target_profile)
        print(f"Downloading posts from @{target_profile}...")
        posts = profile.get_posts()
        downloaded = 0
        for post in posts:
            if count > 0 and downloaded >= count:
                break
            try:
                print(f"Downloading post {post.shortcode} from {post.date}")
                # Save each post in a folder named only by its shortcode, in the current directory
                post_dir = post.shortcode
                orig_pattern = loader.filename_pattern
                loader.filename_pattern = post.shortcode
                loader.download_post(post, target=post_dir)
                loader.filename_pattern = orig_pattern
                downloaded += 1
            except Exception as e:
                print(f"Error downloading post {post.shortcode}: {str(e)}")
                continue
        print(f"Successfully downloaded {downloaded} posts from @{target_profile}")
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Error: Profile @{target_profile} does not exist or is private")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def download_post_by_shortcode(loader, shortcode, save_dir):
    """Download a specific post by its shortcode, saving with the shortcode as filename and folder name in the current directory"""
    try:
        print(f"Downloading post with shortcode {shortcode}...")
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        try:
            print(f"Downloading post from {post.owner_username} posted on {post.date}")
            orig_pattern = loader.filename_pattern
            loader.filename_pattern = shortcode
            post_dir = shortcode  # Folder is just the shortcode, in the current directory
            loader.download_post(post, target=post_dir)
            loader.filename_pattern = orig_pattern
            print(f"Successfully downloaded post {shortcode}")
            return True
        except Exception as e:
            print(f"Error downloading post {shortcode}: {str(e)}")
            return False
    except instaloader.exceptions.BadResponseException:
        print(f"Error: Post with shortcode {shortcode} does not exist or is not accessible")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def extract_shortcode_from_url(url):
    """Extract the shortcode from an Instagram post URL"""
    url = url.strip()
    # Regex matches shortcode and stops at /, ?, or # after it
    pattern = r'(?:https?://)?(?:www\.)?instagram\.com/(?:p|reel|tv)/([A-Za-z0-9_-]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def download_shortcodes_from_file(loader, filepath):
    """Download all posts whose shortcodes are listed in a file (one per line)"""
    if not os.path.exists(filepath):
        print(f"Shortcode file '{filepath}' not found.")
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        shortcodes = [line.strip() for line in f if line.strip()]
    print(f"Found {len(shortcodes)} shortcodes in {filepath}. Starting download...")
    for shortcode in shortcodes:
        download_post_by_shortcode(loader, shortcode, save_dir=".")
    print("All shortcodes processed.")

def main():
    # Parse arguments
    parser = setup_argument_parser()
    args = parser.parse_args()

    # If shortcodes file is provided, process it and exit
    if hasattr(args, 'shortcodes_file') and args.shortcodes_file:
        loader = create_instance(args.username)
        download_shortcodes_from_file(loader, args.shortcodes_file)
        return

    # Check if we have at least one valid target
    if not (args.target or args.shortcode or args.post_url):
        parser.error("You must provide at least one of: -t/--target, -s/--shortcode, or -P/--post-url")
    
    # Create instaloader instance
    loader = create_instance(args.username)
    
    # Process based on what was provided
    if args.post_url:
        # Extract shortcode from URL
        shortcode = extract_shortcode_from_url(args.post_url)
        if shortcode:
            download_post_by_shortcode(loader, shortcode, args.directory)
        else:
            print("Error: Could not extract shortcode from the provided URL")
            sys.exit(1)
    elif args.shortcode:
        # Download by shortcode directly
        download_post_by_shortcode(loader, args.shortcode, args.directory)
    elif args.target:
        # Download from profile
        download_profile_posts(
            loader, 
            args.target, 
            args.directory, 
            args.count,
            args.posts_only
        )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDownload interrupted by user")
        sys.exit(0)
