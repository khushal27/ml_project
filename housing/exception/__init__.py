import sys

class HousingException(Exception):

    def __init__(self,error_message:Exception,error_details:sys):
        super().__init__(error_message)
        self.error_message = HousingException.get_detailed_error_message(error_message=error_message,
        error_details=error_details)


    @staticmethod
    def get_detailed_error_message(error_message:Exception,error_details:sys) ->str:
        _,_,exce_tb = error_details.exc_info()
        line_no = exce_tb.tb_lineno
        filename = exce_tb.tb_frame.f_code.co_filename

        error_msg = f"Exception occured in line : [{line_no}] in the file : [ {filename} ] , error : [{error_message}]"
        return error_msg


    def __str__(self):
        return self.error_message

    def __repr__(self) -> str:
        return HousingException.__name__.str()

    

