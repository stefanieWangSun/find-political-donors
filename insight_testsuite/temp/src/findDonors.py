import sys
import bisect
import datetime

# the three arguments are listed in run.sh
file_path = sys.argv[1]  # input file 
filename_zip = sys.argv[2]  # output file medianvals_by_zip
filename_date = sys.argv[3] # output file medianvals_by_date


# define function for median of each transaction
def median(lst, new):
    bisect.insort(lst, new)
    n = len(lst)
    if n % 2 == 1:
            return lst[n//2],lst
    else:
            return sum(lst[n//2-1:n//2+1])/2.0,lst


# define function to check valid date
def check_date(inputDate):
    correctDate = False
    if inputDate.isdigit() and len(inputDate) == 8:
        year=int(inputDate[4:])
        month=int(inputDate[:2])
        day=int(inputDate[2:4])    
        try:
            datetime.datetime(year, month, day)
            correctDate = True
        except ValueError:
            correctDate = False
    return correctDate



 
if __name__ == "__main__":
    with open(file_path) as file_object:
        lines = file_object.readlines()
    
    append_write ='w'     # for medianvals_by_zip file
    # dictionary with tuple as key 
    ans_zip={} #{ (ID,zip):[ Median, Count, Total, [Amount1, Amount2,...]] }   
    ans_date={} #{ (ID, date):[ Median, Count, Total, [Amount1, Amount2,...]] } 
    for line in lines: # read in each record
        new_record = line.split('|')   
        if new_record[0] !='' and new_record[14] !='' and new_record[15] =='': 
            re_id=new_record[0].upper()  # capitalization
            zip_code=new_record[10][:5]  
            tran_date=new_record[13]  
            amount=float(new_record[14])    
            
# the following code is for medianvals_by_zip        
            if len(zip_code)>=5:           
                if (re_id,zip_code) in ans_zip:
                    list_MCTA=ans_zip[(re_id,zip_code)] # list_MCTA = [median (M), total number (C), Total amount (T), [ Amount1, Amount2,...] ]
                    list_MCTA[0],list_MCTA[3]=median(list_MCTA[3],amount)   # get median and sorted transactions          
                    list_MCTA[1]+=1 # count transaction 
                    list_MCTA[2]+=amount # total amount of transactions
                else:
                    ans_zip[(re_id,zip_code)]=[amount,1,amount,[amount]]
                
                lst=[re_id,zip_code]+ [ round(elem) for elem in ans_zip[(re_id,zip_code)][:3] ] # list contains ID, zip, median, count, total amount
                
                with open(filename_zip, append_write) as file_object:
                    append_write ='a' 
                    file_object.write('|'.join([str(i) for i in lst]))
                    file_object.write('\n')    
    
# the following code is for medianvals_by_date
            if check_date(tran_date):
                if (re_id, tran_date) in ans_date:
                    list_MCTA=ans_date[(re_id,tran_date)] # list_MCTA = [median (M), total number (C), Total amount (T), [ Amount1, Amount2,...] ]
                    list_MCTA[0],list_MCTA[3]=median(list_MCTA[3],amount)             
                    list_MCTA[1]+=1
                    list_MCTA[2]=round(list_MCTA[2]+amount)
                else:
                    ans_date[(re_id,tran_date)]=[amount,1,amount,[amount]]    
            
# sort the key tuple (ID, date) first by ID then by date
        ordered_data = sorted(ans_date.items(), key = lambda x: (x[0][0], datetime.datetime.strptime(x[0][1], '%m%d%Y') ), reverse=False)
    
        with open(filename_date, 'w') as file_object:
            for item in ordered_data:
                lst=list(item[0])+[ round(elem) for elem in item[1][:3] ]
                file_object.write('|'.join([str(i) for i in lst]))
                file_object.write('\n')
        
            
            
            
               
 
    
    
    