import requests
import re
import pandas as pd
import io


class GeneralUtils:
    """
        A class for general purpose functions that can be reused. 
        All functions defined here are to be agnostic, and not specific to a usecase
    """

    @staticmethod    
    def extract_mins(time_value):
        """
            A function to take in a time in PTxxHxxM format and return an integer
            that represents the total time in just minutes. 
            NOTE: any component of the given format is optional.
            eg: PT5H, PT30M, PT12H30M, 8H, 55M are all valid inputs

            Args:
                time_value (string): a given time string in PTxxHxxM format

            Returns:
                int: returns an integer value of the toatl time in minutes
        """

        # Using a combination of caputring and non-caputing groups to extract the time values using regex
        pattern = r'(?:PT)(?:(\d+)H)?(?:(\d+)M)?'
        time_value=time_value.upper()
    
        match = re.search(pattern, time_value)
        if match:
            hours = match.group(1) # Captured group 1 would correspond to Hours according to the re expression above
            minutes = match.group(2)  # Captured group 2 would correspond to Minutes according to the re expression above

            hours = int(hours) if hours is not None else 0
            minutes = int(minutes) if minutes is not None else 0
            hours_in_mins = hours*60 # Converting hours to minutes
            total_mins = minutes+hours_in_mins

            return total_mins
        else:
            return 0
   
    @staticmethod
    def file_fetch(url, save_path=None):
        """
            A function to download the data form a file with the given URL.

            Args:
                url (string): the url of the file whose contents need to be fetched
                save_path (string): OPTIONAL - a path to save the contents of the file locally if needed.

            Returns:
                bytes: returns the contents of the file as bytes
        """

        data=requests.get(url).content
        if save_path:
            with open(save_path, "w") as f:
                f.write(data)
            return data
        return data

    @staticmethod
    def make_dataframe(data):
        """
            A function to convert givent byte data to a Pandas DataFrame.
            NOTE: the byte data must be a valid json or valid json lines file

            Args:
                data (byte): the byte data which needs to be converted form json to a pandas DataFrame

            Returns:
                bytes: returns the contents of the file as bytes
        """
        
        try:
            # Converting the byte data to a buffer stream to be parsed by the read_json function
            byte_stream=io.BytesIO(data)
            df = pd.read_json(byte_stream, lines=True)
            return df
        except Exception as e:
            print("ERROR in parsing data into DataFrame")
            print(e)

    @staticmethod
    def difficulty_label(total_time, hard_cutoff=60, medium_cutoff=30, missing_label="N/A"):
        """
            Generate a difficulty label of Hard, Medium or Easy based on the given total time.

            Args:
                total_time (int): Total time in minutes
                hard_cutoff (int): OPTIONAL (default = 60 mins)- threshold in minutes for the Hard label
                medium_cutoff (int): OPTIONAL (default = 30 mins)- threshold in minutes for the Medium label
                missing_label (int): OPTIONAL (default = N/A)- label for invalid total time, i.e 0 mins or other values

            Returns:
                string: a string lable besed on the given cutoff
        """

        if total_time >= hard_cutoff:
            return "Hard"
        elif total_time >= medium_cutoff:
            return "Medium"
        elif total_time >0:
            return "Easy"
        else:
            return missing_label
 