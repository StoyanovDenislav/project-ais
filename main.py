import subprocess
import Core.speech_recognizer as speech_recognizer
import Core.retrieve_directory_files as retrieve_directory_files

if __name__ == "__main__":
    # Recognize speech
    recognized_text = speech_recognizer.recognize_speech()
    
    
    
    matching_files = retrieve_directory_files.find_files_by_name(recognized_text.lower())

    if matching_files:
        print(f"Files with base name '{recognized_text}' found:")
        for file in matching_files:
            print(file)
    else:
        print(f"No files with base name '{recognized_text}' found in the file system.")