from pathlib import Path
import argparse
from moviepy import VideoFileClip


def zoom_video(input_path, output_path, zoom_factor):
    """
    Zoom in on a video file by the specified zoom factor while preserving audio.

    Args:
        input_path (str): Path to the input video file
        output_path (str): Path to save the zoomed video
        zoom_factor (float): The factor by which to zoom in (e.g., 1.5 for 50% zoom)
    """
    # Load the video with moviepy
    video = VideoFileClip(str(input_path))

    # Get video dimensions
    w, h = video.size

    # Calculate crop dimensions
    crop_width = int(w / zoom_factor)
    crop_height = int(h / zoom_factor)

    # Calculate starting point for cropping (to center the frame)
    x_start = (w - crop_width) // 2
    y_start = (h - crop_height) // 2

    # Apply the zoom effect while preserving audio
    zoomed = video.subclipped()  # Create a copy of the video
    zoomed = zoomed.cropped(
        x1=x_start, y1=y_start, x2=x_start + crop_width, y2=y_start + crop_height
    )
    zoomed = zoomed.resized(width=w, height=h)

    # Write the video with audio
    zoomed.write_videofile(str(output_path), codec="libx264", audio_codec="aac")

    # Close the clips
    video.close()
    zoomed.close()


def process_directory(input_dir, output_dir, zoom_factor):
    """
    Process all video files in the input directory and save zoomed versions to output directory.
    """
    # Create output directory if it doesn't exist
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Video extensions to process
    video_extensions = {".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv"}

    # Process each video file
    input_dir = Path(input_dir)
    for video_file in input_dir.iterdir():
        if video_file.suffix.lower() in video_extensions:
            output_path = output_dir / f"zoomed_{video_file.name}"
            print(f"Processing {video_file.name}...")
            zoom_video(video_file, output_path, zoom_factor)
            print(f"Saved zoomed video to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Zoom in on video files in a directory"
    )
    parser.add_argument(
        "-i",
        "--input-dir",
        required=True,
        help="Input directory containing video files",
    )
    parser.add_argument(
        "-o", "--output-dir", required=True, help="Output directory for zoomed videos"
    )
    parser.add_argument(
        "-z",
        "--zoom",
        type=float,
        default=1.5,
        help="Zoom factor (e.g., 1.5 for 50% zoom, default: 1.5)",
    )

    args = parser.parse_args()
    process_directory(args.input_dir, args.output_dir, args.zoom)


if __name__ == "__main__":
    main()
