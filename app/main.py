import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select, func
from .db import Base, engine, SessionLocal
from .models import Merchant, Product, Order
from .bot import build_application, start_bot

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    await start_bot()
    yield

app = FastAPI(title="SL Market", version="0.1.0", lifespan=lifespan)

@app.get("/", response_class=HTMLResponse)
def home():
    return '''
    <!doctype html><html lang="so"><head><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>SL Market Admin</title><style>
    body{font-family:Arial;background:#f3f5f8;margin:0;color:#172033}
    header{background:#10233f;color:white;padding:22px}main{padding:18px;max-width:900px;margin:auto}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}
    .card{background:white;border-radius:12px;padding:18px;box-shadow:0 2px 10px #0001}
    .num{font-size:28px;font-weight:bold;margin-top:8px}small{color:#64748b}
    </style></head><body><header><h2>SL Market</h2><small>Admin dashboard · MVP</small></header>
    <main><h3>Guudmarka suuqa</h3><div class="grid">
    <div class="card">Ganacsato<div class="num" id="m">—</div></div>
    <div class="card">Alaabo<div class="num" id="p">—</div></div>
    <div class="card">Dalabaad<div class="num" id="o">—</div></div></div>
    <p><small>Dashboard-kan waa bilowga; qaybaha amniga iyo maamulka buuxa waxaa lagu daraa marxaladda xigta.</small></p>
    </main><script>
    fetch('/api/stats').then(r=>r.json()).then(x=>{m.textContent=x.merchants;p.textContent=x.products;o.textContent=x.orders})
    </script></body></html>'''

@app.get("/health")
def health():
    return {"status": "ok", "service": "sl-market"}

@app.get("/api/stats")
def stats():
    with SessionLocal() as db:
        return {
            "merchants": db.scalar(select(func.count()).select_from(Merchant)) or 0,
            "products": db.scalar(select(func.count()).select_from(Product)) or 0,
            "orders": db.scalar(select(func.count()).select_from(Order)) or 0,
        }

@app.get("/api/shops")
def shops():
    with SessionLocal() as db:
        rows = db.scalars(select(Merchant).where(Merchant.active == True).order_by(Merchant.name)).all()
        return [{"id":x.id,"name":x.name,"city":x.city,"slug":x.shop_slug} for x in rows]

@app.get("/api/products")
def products():
    with SessionLocal() as db:
        rows = db.execute(select(Product, Merchant).join(Merchant).where(Product.available == True).order_by(Product.created_at.desc()).limit(100)).all()
        return [{"id":p.id,"title":p.title,"price":float(p.price),"currency":p.currency,"shop":m.name,"city":m.city} for p,m in rows]
