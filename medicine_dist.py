med_stock = {
    "Paracetamol":50,"Dolo":29,"Ondem":30,"Burnol":12,"Betadine":32,"Auntyy":1
    }

def check_stock():
  for i,j in med_stock.items():
    if(j<10):
        print(f"Please refill stocks!! {i}{j}")        

(check_stock())
        
        
