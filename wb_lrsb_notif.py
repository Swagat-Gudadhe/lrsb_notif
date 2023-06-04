from datetime import datetime as dt
from datetime import timedelta
import json
import pandas as pd
import smtplib
from logzero import logger, logfile
import fbnotify  as fb
fbnotify = fb.notification()
notif_sent=False


notif_sent=False
def early_notif():
    global apiEntry
    global notif_sent

    if 'mailTS' in (apiEntry['output']) and 'plantLRSBTiming' in (apiEntry['input']):

        if (pd.to_datetime(dt.strptime(apiEntry['output']['mailTS'][-1]["Time"],'%Y-%m-%d %H:%M:%S'))) < (pd.to_datetime(dt.strptime(apiEntry['input']['plantLRSBTiming'][-1]['end'],'%Y-%m-%d %H:%M:%S'))):
            expect_reco_after = (pd.to_datetime(dt.strptime(apiEntry['input']['plantLRSBTiming'][-1]['end'],'%Y-%m-%d %H:%M:%S')))+ (timedelta(seconds=apiEntry['input']['LRSB_CYCLE_THRESHOLD']))
        else:
            expect_reco_after = (pd.to_datetime(dt.strptime(apiEntry['output']['mailTS'][-1]["Time"],'%Y-%m-%d %H:%M:%S')))+ (timedelta(seconds=apiEntry['input']['LRSB_CYCLE_THRESHOLD']))

        logger.info('Last blower operated={}'.format(apiEntry['input']['plantLRSBTiming'][-1]['end'],'%Y-%m-%d %H:%M:%S'))
        logger.info('Last SB mail sent={}'.format(apiEntry['output']['mailTS'][-1]["Time"],'%Y-%m-%d %H:%M:%S'))
        logger.info('LRSB cycle threshold={}'.format(apiEntry['input']['LRSB_CYCLE_THRESHOLD']))
        
        mail="SB"
    else:
        if (pd.to_datetime(dt.strptime(apiEntry['input']['wbSB'][-1]["Time"],'%Y-%m-%d %H:%M:%S'))) < (pd.to_datetime(dt.strptime(apiEntry['input']['plantWBTiming'][-1]['end'],'%Y-%m-%d %H:%M:%S'))):
             expect_reco_after = (pd.to_datetime(dt.strptime(apiEntry['input']['plantWBTiming'][-1]['end'],'%Y-%m-%d %H:%M:%S')))+ (timedelta(seconds=apiEntry['input']['WB_CYCLE_THRESHOLD']))
        else:
            expect_reco_after = (pd.to_datetime(dt.strptime(apiEntry['input']['wbSB'][-1]["Time"],'%Y-%m-%d %H:%M:%S'))) + (timedelta(seconds=apiEntry['input']['WB_CYCLE_THRESHOLD']))

        logger.info('Last blower operated={}'.format(apiEntry['input']['plantWBTiming'][-1]['end'],'%Y-%m-%d %H:%M:%S'))
        logger.info('Last WB mail sent={}'.format(apiEntry['input']['wbSB'][-1]["Time"],'%Y-%m-%d %H:%M:%S'))
        logger.info('WB cycle threshold={}'.format(apiEntry['input']['WB_CYCLE_THRESHOLD']))
        
        mail="WB"
        

    notification_time = expect_reco_after - timedelta(seconds=5400)
    current_time=dt.now().replace(second=0, microsecond=0) + timedelta(hours=5.5)
    remaining_time=notification_time-current_time
    

    logger.info('Expect next '+mail+' mail after={}'.format(expect_reco_after))
    logger.info('Current time={}'.format(current_time))
    logger.info('Notification time ={}'.format(notification_time))
    
    if not notif_sent and current_time == notification_time:
        
        fbnotify.setNotification({"title":"Preparatory notification","body":"Expect SB recommendation mail after 90 min"})
        fbnotify.setData({"message":"next recommendation will occur in X minutes from now basis last reco or last blower operated."})
        logger.info("Current time is equal to notification time.")
        
        try:
            fbnotify.sendMessage()
            logger.info(mail+" Preparatory countdown timer notification sent successfully")
            notif_sent = False

        except Exception as e: 
            logger.info(str(e))
            logger.info("EXCEPTION: Unable to send LRSB Preparatory countdown timer notification")
    else:
        logger.info("Current time is not equal to notification time,cannot trigger notification.")
        logger.info('Time remain to send '+mail+' notification={}'.format(remaining_time))
        



# def notif(plSBTime,mailTS, LRSB_CYCLE_THRESHOLD): 
#     plSBTime = pd.to_datetime(datetime.datetime.strptime(plSBTime, '%Y-%m-%d %H:%M:%S'))
#     mailTS= pd.to_datetime(datetime.datetime.strptime(mailTS, '%Y-%m-%d %H:%M:%S'))
#     LRSB_CYCLE_THRESHOLD = datetime.timedelta(seconds=LRSB_CYCLE_THRESHOLD)
#     current_time = datetime.datetime.now().replace(microsecond=0)
    
#     if mailTS<plSBTime:
#         next_mail_sent = plSBTime + LRSB_CYCLE_THRESHOLD
#     else:
#         next_mail_sent = mailTS + LRSB_CYCLE_THRESHOLD

#     notification_time = next_mail_sent - datetime.timedelta(seconds=5400)


#     logger.info('last lrsb blorwer operated on ={}:'.format(plSBTime))
#     logger.info('last sootblowing mail sent on ={}:'.format(mailTS))
#     logger.info('next mail to be sent on={}'.format(next_mail_sent))
#     logger.info('LRSB cycle thresh={}'.format(LRSB_CYCLE_THRESHOLD))j

#     logger.info('notification for the recomendation mail to be sent on ={}'.format(notification_time))
#     logger.info('current time={}'.format(current_time))
    

#     sender = 'optimus24.prime248@gmail.com'
#     receivers = ['swagatgudadhe@gmail.com']
#     message= ' Next recommendation will occur in 90 minutes from now basis last reco or last blower operated.'

#     s= smtplib.SMTP('smtp.gmail.com',25)
#     s.ehlo()
#     s.starttls()
#     s.login('optimus24.prime248@gmail.com','bxgguqskmztwymxf')

    
#     if current_time == notification_time:
    
#         s.sendmail(sender,receivers,message)
#         return('msg sent')
#     else:

#         return('time remain to send notification',notification_time-current_time)
    



# s=notif('2023-05-15 02:02:00','2023-05-14 16:09:45',43200)
# logger.info(s)