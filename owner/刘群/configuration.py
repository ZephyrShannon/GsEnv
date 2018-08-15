# <codecell>




def configuration(start_date = "2015/07/01",volume_average_days = 30,feature_number = 3,end_date = "2017/07/01",global_period = 1800,\
                  test_portion=0.2,window_size = 31,training_learning_rate=0.00028,training_buffer_biased=5e-05,training_method='Adam',\
                  batch_size=109,steps=10000 ,rolling_training_steps=85 ,trading_consumption=0.0025,trading_buffer_biased=5e-05,\
                  trading_learning_rate=0.00028):
    market = "not poloniex "                
    coin_number = 338    
    online = 'false'       
    snap_shot='false'    
    fast_train='true'    
    loss_function='loss_function6'   
    type_0='ConvLayer' 
    filter_shape=[1,2]
    filter_number_0=3
    weight_decay_1=5e-9
    type_1='EIIE_Dense'
    filter_number_1=10
    regularizer_1='L2'
    weight_decay_2 = 5e-08
    type_2='EIIE_Output_WithW'
    regularizer_2='L2'
    
    
    config_dic={"input": {"start_date": start_date, "volume_average_days": volume_average_days, "market": market, \
                          "feature_number": feature_number, "end_date": end_date, "coin_number": coin_number,
                          "global_period": global_period, "online": online, "test_portion":test_portion,\
                          "window_size": window_size}, \
                "training": {"snap_shot": snap_shot, "learning_rate": training_learning_rate, "buffer_biased": training_buffer_biased, \
                             "training_method": training_method, "fast_train": fast_train, "batch_size": batch_size, \
                             "loss_function": loss_function, "steps": steps}, \
                "layers": [{"type": type_0, "filter_shape": filter_shape, "filter_number": filter_number_0},\
                           {"weight_decay": weight_decay_1, "type":type_1, "filter_number": filter_number_1, "regularizer": regularizer_1}, \
                           {"weight_decay": weight_decay_2, "type": type_2, "regularizer": regularizer_2}], \
                "trading": {"rolling_training_steps": rolling_training_steps, "trading_consumption": trading_consumption, \
                            "buffer_biased": trading_buffer_biased, "learning_rate": trading_learning_rate}}
    return config_dic 
      
    

# <codecell>

