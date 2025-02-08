import cv2
import os
from pathlib import Path
import argparse

def zoom_video(input_path, output_path, zoom_factor):
    """
    Zoom in on a video file by the specified zoom factor.
    
    Args:
        input_path (str): Path to the input video file
        output_path (str): Path to save the zoomed video
        zoom_factor (float): The factor by which to zoom in (e.g., 1.5 for 50% zoom)
    """
    # Open the video
    cap = cv2.VideoCapture(str(input_path))
    if not cap.isOpened():
        print(f"Error: Could not open video {input_path}")
        return

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Calculate new dimensions
    new_width = frame_width
    new_height = frame_height
    
    # Calculate crop dimensions
    crop_width = int(frame_width / zoom_factor)
    crop_height = int(frame_height / zoom_factor)
    
    # Calculate starting point for cropping (to center the frame)
    x_start = (frame_width - crop_width) // 2
    y_start = (frame_height - crop_height) // 2

    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(output_path), fourcc, fps, (new_width, new_height))

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Crop the frame
            cropped = frame[y_start:y_start + crop_height, x_start:x_start + crop_width]
            
            # Resize back to original dimensions
            zoomed = cv2.resize(cropped, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
            
            # Write the frame
            out.write(zoomed)

    finally:
        # Release everything
        cap.release()
        out.release()

def process_directory(input_dir, output_dir, zoom_factor):
    """
    Process all video files in the input directory and save zoomed versions to output directory.
    """
    # Create output directory if it doesn't exist
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Video extensions to process
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv'}
    
    # Process each video file
    input_dir = Path(input_dir)
    for video_file in input_dir.iterdir():
        if video_file.suffix.lower() in video_extensions:
            output_path = output_dir / f"zoomed_{video_file.name}"
            print(f"Processing {video_file.name}...")
            zoom_video(video_file, output_path, zoom_factor)
            print(f"Saved zoomed video to {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Zoom in on video files in a directory')
    parser.add_argument('-i', '--input-dir', required=True,
                        help='Input directory containing video files')
    parser.add_argument('-o', '--output-dir', required=True,
                        help='Output directory for zoomed videos')
    parser.add_argument('-z', '--zoom', type=float, default=1.5,
                        help='Zoom factor (e.g., 1.5 for 50%% zoom, default: 1.5)')
    
    args = parser.parse_args()
    process_directory(args.input_dir, args.output_dir, args.zoom)

if __name__ == "__main__":
    main()


