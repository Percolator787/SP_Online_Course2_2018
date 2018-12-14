"""
    demonstrate use of Redis
"""


import login_database
import utilities


def run_example():
    """
        uses non-presistent Redis only (as a cache)

    """

    log = utilities.configure_logger('default', '../logs/redis_script.log')

    try:
        log.info('Step 1: connect to Redis')
        r = login_database.login_redis_cloud()
        log.info('Step 2: cache some data in Redis')
        r.set('andy', 'andy@somewhere.com')

        log.info('Step 2: now I can read it')
        email = r.get('andy')
        log.info('But I must know the key')
        log.info(f'The results of r.get: {email}')

        log.info('Step 3: cache more data in Redis')
        r.set('pam', 'pam@anywhere.com')
        r.set('fred', 'fred@fearless.com')

        log.info('Step 4: delete from cache')
        r.delete('andy')
        log.info(f'r.delete means andy is now: {email}')

        log.info(
            'Step 6: Redis can maintain a unique ID or count very efficiently')
        r.set('user_count', 21)
        r.incr('user_count')
        r.incr('user_count')
        r.decr('user_count')
        result = r.get('user_count')
        log.info('I could use this to generate unique ids')
        log.info(f'Redis says 21+1+1-1={result}')

        log.info('Step 7: richer data for a SKU')
        r.rpush('186675', 'chair')
        r.rpush('186675', 'red')
        r.rpush('186675', 'leather')
        r.rpush('186675', '5.99')

        log.info('Step 8: pull some data from the structure')
        cover_type = r.lindex('186675', 2)
        log.info(f'Type of cover = {cover_type}')

        log.info('Step 8: Add customer name, phone, and zip code to redis')
        r.hmset('Max', {'phone':'2063331111', 'zip':'98057'})
        r.hmset('Jenny', {'phone':'4251110000', 'zip':'98144'})
        r.hmset('Elf', {'phone':'2539990000', 'zip': '94115'})
        r.hmset('Santa',{'phone':'4138889999', 'zip': '99045'})
        r.hmset('Ralph', {'phone':'3411234567', 'zip': '98711'})
        r.hmset('Winston', {'phone':'1230009999', 'zip': '98114'})

        log.info('Retrieve customer Jenny')
        my_dict = r.hgetall('Jenny')
        msg = []
        for k, v in my_dict.items():
            msg.append('Phone: ')
            msg.append(k)
            msg.append('Zip: ')
            msg.append(v)
        log.info('\t'.join(msg))

    except Exception as e:
        print(f'Redis error: {e}')
