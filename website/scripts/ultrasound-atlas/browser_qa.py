#!/usr/bin/env python3
"""Smoke-test the built Astro atlas, including actual user-triggered GLB loads.
Requires Playwright + its Chromium binary. Never marks medical review complete.
"""
from __future__ import annotations
import base64, io, json, threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[3]
PUBLIC=ROOT/'website/public/medical-visuals/ultrasound'
DIST=ROOT/'website/dist'
QA=ROOT/'website/qa/ultrasound-atlas'

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass


def main():
    if not (DIST/'ultrasound-atlas/index.html').exists():raise FileNotFoundError('Build the Astro website first')
    QA.mkdir(parents=True,exist_ok=True)
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(DIST)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    origin=f'http://127.0.0.1:{server.server_port}'
    report={'status':'pass','clinicalReview':'needs-clinician-review','static':[],'models':[],'articleImages':0}
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,args=['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-webgl'])
            for width in [390,1440]:
                page=browser.new_page(viewport={'width':width,'height':1000},reduced_motion='reduce')
                requests=[];page.on('request',lambda r:requests.append(r.url))
                response=page.goto(origin+'/ultrasound-atlas/');assert response and response.status==200
                page.wait_for_selector('.region');assert page.locator('.region').count()==6
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'),'Horizontal overflow'
                for image in page.locator('.region > figure img').all():
                    image.scroll_into_view_if_needed();image.evaluate('(i)=>i.decode()')
                    assert image.evaluate('(i)=>i.naturalWidth===1800 && i.alt.length>20')
                assert not any('.glb' in url for url in requests),'Models loaded before user request'
                page.locator('nav[aria-label="選擇關節"] a[href="#ankle"]').click()
                assert page.url.endswith('#ankle')
                page.evaluate('window.scrollTo(0,0)');page.screenshot(path=str(QA/f'atlas-{width}.png'))
                report['static'].append({'viewport':width,'images':6,'overflow':False,'noAutomaticGLBDownloads':True,'anchors':'pass'})
                page.close()
            page=browser.new_page(viewport={'width':1440,'height':1100},reduced_motion='reduce')
            errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
            page.goto(origin+'/ultrasound-atlas/');page.wait_for_selector('.region')
            for section in page.locator('.region').all():
                region=section.get_attribute('id');section.locator('details.models > summary').click()
                for index,root in enumerate(section.locator('[data-medical-model]').all()):
                    mode=['long','short'][index];enable=root.locator('[data-enable]')
                    enable.click();page.wait_for_function('(el)=>el.textContent.includes("3D 已載入")',arg=root.locator('[data-status]').element_handle(),timeout=60000)
                    viewer=root.locator('model-viewer');assert viewer.evaluate('(el)=>el.loaded===true')
                    viewer.evaluate('(el)=>el.updateComplete')
                    viewer.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
                    data=viewer.evaluate('(el)=>el.toDataURL("image/png")')
                    png=base64.b64decode(data.split(',',1)[1]);im=Image.open(io.BytesIO(png)).convert('RGB')
                    assert np.asarray(im).std()>8,'Blank model screenshot'
                    (QA/f'{region}-{mode}-webgl.png').write_bytes(png)
                    root.locator('[data-action="right"]').click();root.locator('[data-action="reset"]').click()
                    assert viewer.evaluate('(el)=>Number.isFinite(el.getCameraOrbit().radius)')
                    enable.click();assert root.locator('model-viewer').count()==0
                    report['models'].append({'region':region,'axis':mode,'loaded':True,'nonblank':True,'rotateReset':'pass'})
                section.locator('details.models > summary').click()
            assert not errors,'Browser errors: '+repr(errors)
            page.goto(origin+'/articles/msk-ultrasound-self-study/')
            images=page.locator('img[src^="/medical-visuals/ultrasound/"]')
            assert images.count()==6
            for image in images.all():image.scroll_into_view_if_needed();image.evaluate('(i)=>i.decode()')
            report['articleImages']=images.count();page.close();browser.close()
        (PUBLIC/'browser-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({'browserQA':'pass','viewports':2,'actualWebGLModels':12,'articleImages':6,'clinicalReview':'needs-clinician-review'},ensure_ascii=False))
    finally:server.shutdown()

if __name__=='__main__':main()
