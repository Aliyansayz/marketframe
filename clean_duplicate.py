if len(matches_s) > 0 and len(matches_b) > 0 :
               matches_s , matches_b  =  cls.clean_duplicate(find_s, find_b )
        def clean_duplicate(find_s, find_b):
          up_index    = np.where(find_b)[0]
          down_index  = np.where(find_s)[0]


          if up_index[-1] > down_index[-1]:   matches_s, matches_b = [] , data[find_b]
          elif up_index[-1] < down_index[-1]: matches_s, matches_b =  data[find_s] , []

          return  matches_s, matches_b
