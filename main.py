from Framework import CFramework

framework = CFramework.instance()
app = framework.getFastApiApp()

if __name__ == "__main__":
   import uvicorn
   uvicorn.run(app, port=80)