import os
import uvicorn
import config

if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=config.PORT, debug=config.DEBUG, reload=True, workers=os.cpu_count()*2+1)
