#!/usr/bin/env python
# coding: utf-8

# In[1]:


from crontab import CronTab


# In[16]:


cron = CronTab(tabfile='* * * * *')


# In[17]:


job = cron.new(command='update_odds.py')
job.minute.every(10)

cron.write()


# In[ ]:





# In[ ]:




