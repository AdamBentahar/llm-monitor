import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime

from backend.collector.run import run_pipeline
from backend.reports.generator import generate_report

scheduler = BlockingScheduler()

def daily_job():
    print(f"\n🔄 Running daily pipeline at {datetime.now().strftime('%Y-%m-%d %H:%M')}...")
    try:
        run_pipeline()
        print("✅ Collection complete!")
    except Exception as e:
        print(f"❌ Collection error: {e}")
    
    try:
        generate_report()
        print("✅ Report generated!")
    except Exception as e:
        print(f"❌ Report error: {e}")
    
    print("🎉 Daily job completed!")

# Run immediately on start
print("🚀 LLM Monitor Scheduler starting...")
print("⏰ Pipeline will run every 24 hours")
print("▶️ Running first execution now...")
daily_job()

# Schedule for every 24 hours
scheduler.add_job(
    daily_job,
    trigger=IntervalTrigger(hours=24),
    id="daily_pipeline",
    name="Daily LLM Collection & Report"
)

if __name__ == "__main__":
    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("\n⛔ Scheduler stopped.")
        scheduler.shutdown()