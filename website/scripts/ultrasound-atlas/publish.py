"""Generate indexes and make narrowly scoped, idempotent article insertions."""
from __future__ import annotations
import html, json, re
from pathlib import Path
from catalog import ITEMS, DATE, ESSR, AIUM

BEGIN='<!-- ultrasound-atlas:start -->'
END='<!-- ultrasound-atlas:end -->'
BASE='/medical-visuals/ultrasound/'
NOTICE='AI 輔助製作的概念性教學素材，尚待程皓醫師審閱；不是患者影像、標準化完整檢查流程或操作認證。'

PAGE='''---
import BaseLayout from '@/layouts/BaseLayout.astro';
import MedicalModel from '@/components/MedicalModel.astro';
import atlas from '../../public/medical-visuals/ultrasound/manifest.json';
const base = '/medical-visuals/ultrasound/';
const modes = ['long', 'short'] as const;
const modeName = { long: '長軸', short: '短軸' };
---
<!-- ultrasound-atlas:generated-page -->
<BaseLayout title="超音波六部位：立體解剖與探頭位置" description="肩、肘、腕、髖、膝、踝的原創超音波教學圖卡，含長短軸探頭位置與可旋轉 GLB 概念模型。尚待醫師審閱。">
  <div class="atlas container">
    <header>
      <p class="eyebrow">DOCTOR HAO / MSK ULTRASOUND ATLAS</p>
      <h1>六個部位，從解剖到探頭位置。</h1>
      <p class="lede">每一部位選定一個代表性視窗，並排觀察長軸、短軸與方向標記。六張圖卡與十二個可旋轉模型變體，均來自同一組原創三維幾何。</p>
      <p class="notice"><strong>示意草稿・尚待程皓醫師審閱。</strong>模型結構與比例經簡化，不是病人影像或聲學模擬。完整六部位系列不等於完整臨床檢查；不能據此診斷、量測或自行進行侵入性處置。</p>
      <p><a href="/articles/msk-ultrasound-self-study/">回到超音波自學文章</a> · <a href="/medical-visuals/">全部醫學素材</a></p>
      <nav aria-label="選擇關節">{atlas.items.map(v => <a href={`#${v.id}`}>{v.name}</a>)}</nav>
    </header>
    {atlas.items.map((v, i) => <section id={v.id} class="region" aria-labelledby={`${v.id}-title`}>
      <p class="eyebrow">{String(i + 1).padStart(2, '0')} / 06</p>
      <h2 id={`${v.id}-title`}>{v.name}：{v.target}</h2>
      <figure>
        <a href={base + v.png} aria-label={`開啟${v.name}大圖`}>
          <picture><source srcset={base + v.image} type="image/webp" /><img src={base + v.png} width="1800" height="1200" alt={v.alt} loading="lazy" decoding="async" /></picture>
        </a>
        <figcaption>{v.alt}</figcaption>
      </figure>
      <div class="reading"><div><h3>擺位與辨識</h3>{v.position.map(t => <p>{t}</p>)}{v.caution.map(t => <p>{t}</p>)}</div>
        <div><h3>其他區域的閱讀路線</h3><dl>{v.windows.map(([region, targets]) => <><dt>{region}</dt><dd>{targets}</dd></>)}</dl><p class="small">此清單用於銜接文章資源；本組 3D 模型僅示範上方主視窗，未提供清單中每一視窗的完整操作示範。</p></div></div>
      <details class="models"><summary>展開{v.name}的長、短軸 3D 模型</summary>
        <p class="small">方向標記為本系列的顯示約定；須與實際設備、側別及科室規範核對。局部皮膚接觸片是分層示意，不是病人皮膚模型。</p>
        <div class="model-grid">{modes.map(mode => <div><h3>{modeName[mode]}探頭位置</h3><MedicalModel src={base + v.models[mode]} poster={`${base}${v.id}-${mode}-poster.webp`} alt={`${v.name}${modeName[mode]}探頭位置，概念性三維解剖示意。`} notes="不模擬超音波聲束传播、組織變形或診斷結果；圖中解剖不完整且不能量測。" camera={v.camera} /></div>)}</div>
      </details>
      <p class="downloads"><a href={base + v.svg} download>SVG 圖卡</a><a href={base + v.png} download>PNG 圖卡</a><a href={base + v.image} download>WebP 圖卡</a></p>
      <p class="small">查核來源：<a href={v.references[0].url} target="_blank" rel="noopener noreferrer">ESSR {v.name}技術指引</a>（{v.references[0].locator}）；<a href={v.references[1].url} target="_blank" rel="noopener noreferrer">AIUM 2023 MSK Practice Parameter</a>。</p>
    </section>)}
    <footer class="small"><p>青色平面不表示積液，暖色不表示病變分級；沒有合成 B 模式超音波影像。參考文件是製作依據，不代表學會背書。</p><p>版本：{atlas.created} · 審閱狀態：尚待醫師審閱 · <a href={base + 'manifest.json'}>素材索引與 SHA-256</a></p></footer>
  </div>
</BaseLayout>
<style>
  .atlas { padding-block: 3rem; max-width: 1200px; }
  .eyebrow { color: #297c86; font-size: .8rem; letter-spacing: .1em; font-weight: 700; }
  h1 { font-size: clamp(2rem,5vw,3.3rem); line-height: 1.3; max-width: 18em; }
  .lede { font-size: 1.15rem; line-height: 1.9; max-width: 50em; }
  .notice { background: #fff3df; color: #765321; border-radius: 14px; padding: 1.1rem 1.3rem; line-height: 1.9; }
  nav, .downloads { display: flex; flex-wrap: wrap; gap: 1rem; }
  nav { margin-block: 2rem; } nav a { padding: .65rem 1rem; border: 1px solid var(--c-line,#cbd9de); border-radius: 10px; }
  .region { border-top: 1px solid var(--c-line,#cbd9de); padding-block: 2rem; scroll-margin-top: 6rem; }
  h2 { font-size: clamp(1.5rem,3vw,2rem); line-height: 1.5; }
  figure { margin: 1.5rem 0; } figure img { display: block; width: 100%; height: auto; border-radius: 16px; }
  figcaption, .small { font-size: .88rem; line-height: 1.8; color: var(--c-muted,#50666e); }
  figcaption { margin-top: .7rem; } .reading, .model-grid { display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: 2rem; }
  .reading p { line-height: 1.85; } dl { display: grid; grid-template-columns: 5em 1fr; gap: .6rem; line-height: 1.8; } dt { font-weight: 600; } dd { margin: 0; }
  .models { margin-block: 1rem; padding: 1.1rem; border: 1px solid var(--c-line,#cbd9de); border-radius: 12px; }
  summary { cursor: pointer; min-height: 44px; font-weight: 600; }
  a:focus-visible, summary:focus-visible { outline: 3px solid #168195; outline-offset: 4px; }
  @media (max-width: 760px) { .reading,.model-grid { grid-template-columns: 1fr; } .atlas { padding-block: 2rem; } }
</style>
'''.replace('传播','傳播')


def replace_block(path:Path,body:str,anchor:str|None=None):
    old=path.read_text(encoding='utf-8')
    if old.count(BEGIN)!=old.count(END) or old.count(BEGIN)>1:raise ValueError(f'Unexpected atlas markers: {path}')
    block=BEGIN+'\n'+body.rstrip()+'\n'+END
    if BEGIN in old:
        new=re.sub(re.escape(BEGIN)+r'.*?'+re.escape(END),lambda _:block,old,flags=re.S)
    elif anchor:
        if old.count(anchor)!=1:raise ValueError(f'Expected one integration anchor in {path}')
        new=old.replace(anchor,block+'\n\n'+anchor,1)
    else:new=old+('\n' if old.endswith('\n') else '\n\n')+block+'\n'
    path.write_text(new,encoding='utf-8')


def article_section(archive=False):
    lines=['## 肩／肘／腕／髖／膝／踝：立體解剖與探頭位置', '', '> '+NOTICE,
           '> 每部位以一個代表性視窗呈現長、短軸；不是把一張圖當作完整的關節檢查。', '']
    if not archive:lines += ['[開啟六部位 3D 圖解館與可旋轉模型](/ultrasound-atlas/)', '']
    for it in ITEMS:
        name=it['id']+'-anatomy-probe'
        lines += ['### '+it['name']+'：'+it['target'],'']
        if archive:lines += [f'![{it["summary"]}](../medical_3d_assets/ultrasound/{name}.svg)','']
        else:lines += [f'<figure><a href="{BASE}{name}.png"><picture><source srcset="{BASE}{name}.webp" type="image/webp" /><img src="{BASE}{name}.png" width="1800" height="1200" loading="lazy" decoding="async" alt="{html.escape(it["summary"],quote=True)}" /></picture></a><figcaption>{html.escape(it["summary"])}</figcaption></figure>','']
        lines += ['**擺位概念：**'+''.join(it['position']),'', '**定位提醒：**'+''.join(it['caution']),'',f'[ESSR {it["name"]}技術指引]({ESSR}{it["id"]}.pdf)（{it["reference_pages"]}）。','']
    lines += ['### 使用範圍與來源','',
       '圖像與模型採簡化的成人解剖，沒有個案資料，也沒有合成 B 模式影像。探頭長邊、切面及標記只示意相對方向；正式檢查仍需由受訓人員依病史、理學檢查、設備設定與適應症完成，不能依本圖自行診斷或施作注射。','',
       f'跨部位原則參考 [AIUM 2023 肌肉骨骼超音波 Practice Parameter]({AIUM})。ESSR 文件為既有技術指引，本系列沒有宣稱其為 2026 年新發布版本。','',f'素材新增日期：{DATE}。醫學審閱：**尚未完成**。']
    return '\n'.join(lines)


def publish(root,out,archive,manifest,integrate=True):
    readme=['# 超音波六部位：立體解剖＋探頭位置','',NOTICE,'',
      '本系列提供 6 張 1800×1200 圖卡（SVG / PNG / WebP）、12 個 GLB 模型變體（6 部位 × 長短軸）及 12 張延遲載入海報。GLB 是可旋轉的真實三維網格；SVG 的文字可編輯，三维場景以內嵌 PNG 保存。'.replace('三维','三維'),'',
      '**範圍界線：**六部位都有素材，但每部位只建模一個代表性視窗。另列 24 項區域閱讀路線，並未建模全部診斷視窗或完整人體。','',
      '[開啟靜態圖庫](index.html) · 網站建置後的互動路徑：`/ultrasound-atlas/` · [索引與雜湊](manifest.json)','',
      '| 部位 | 核心視窗 | 圖卡 | GLB |','|---|---|---|---|']
    for v in manifest['items']:readme.append(f'| {v["name"]} | {v["target"]} | [PNG]({v["png"]}) / [SVG]({v["svg"]}) / [WebP]({v["image"]}) | [長軸]({v["models"]["long"]}) / [短軸]({v["models"]["short"]}) |')
    readme += ['', '## 醫學與技術界線','',
      '幾何形狀、組織厚度與比例均經簡化；局部皮膚接觸片僅用於解釋探頭接觸與切面。青色平面不是積液、不是診斷圖像，也不模擬聲束衰減、折射或回音。暖色不是疾病分級。模型不含針具、穿刺路徑或治療劑量。', '',
      '腕隧道模型包含 4 條 FDS、4 條 FDP、1 條 FPL 與正中神經；支持帶透明化是為了可讀性。沒有把尺神經、尺動脈或橈側屈腕肌腱放入腕隧道。髖模型是成人前方視窗。膝模型未移開髕骨，不以此評估完整十字韌帶或半月板。', '',
      '方向標記是本系列的約定，不宣稱所有設備或科室均相同。GLB 採 Y-up；單位為任意設計單位，不可量測。模型的機器檢查通過不代表臨床內容通過審查。', '',
      '## 來源與權利','',
      '圖像由專案中的原創參數化幾何生成，不複製學會 PDF 圖片、醫療影像、影片截圖或第三方模型，也不包含個資。引用參考文件不表示學會或程皓醫師背書。沒有另外替既有專案或第三方資料變更授權。', '',
      f'- [AIUM 2023 Practice Parameter]({AIUM})：一般掃描與多切面原則。']
    for v in manifest['items']:readme.append(f'- [ESSR {v["name"]}]({v["references"][0]["url"]})：{v["references"][0]["locator"]}。')
    readme += ['', '## 重建','', '從版本庫根目錄執行：','', '```sh','python -m pip install -r website/scripts/ultrasound-atlas/requirements.txt','python website/scripts/ultrasound-atlas/build.py','python website/scripts/ultrasound-atlas/validate.py','cd website && npm ci && npm run build','```','',
      '可用 `--only shoulder --no-integrate` 重建單一部位，供繪圖測試；發布時必須不帶 `--only` 重建全系列及索引。CI 只提交本系列的白名單路徑，保留其他醫學素材、文章與原始 HTML。推送 GitHub 不等於已發布至外部 Blogger 網站。','',
      '生成工具：Python、NumPy、VTK、trimesh、CairoSVG、Pillow。不同字型與圖形驅動環境的光柵輸出可能不同；manifest 中的 SHA-256 對應該次實際生成檔。沒有打包字型檔。','']
    (out/'README.md').write_text('\n'.join(readme),encoding='utf-8')
    archive_readme=['# 超音波六部位系列','',NOTICE,'',
       '此目錄保留六張文章用 SVG。完整 PNG / WebP、可旋轉 GLB 與來源位於 [網站素材目錄](../../../website/public/medical-visuals/ultrasound/README.md)。','',
       'SVG 圖卡內含三維模型渲染及可編輯文字，不是可旋轉 SVG；需要互動時請使用 GLB 或網站 `/ultrasound-atlas/`。','']
    for v in manifest['items']:archive_readme += [f'## {v["name"]}：{v["target"]}',f'![{v["alt"]}]({v["svg"]})','']
    (archive/'README.md').write_text('\n'.join(archive_readme),encoding='utf-8')
    tiles=[]
    for v in manifest['items']:
        tiles.append(f'<section id="{v["id"]}"><h2>{v["name"]}：{html.escape(v["target"])}</h2><a href="{v["png"]}"><img src="{v["image"]}" width="1800" height="1200" alt="{html.escape(v["alt"],quote=True)}" loading="lazy"/></a><p>{html.escape(v["alt"])}</p><p><a href="{v["svg"]}">SVG</a> · <a href="{v["png"]}">PNG</a> · <a href="{v["models"]["long"]}" download>長軸 GLB</a> · <a href="{v["models"]["short"]}" download>短軸 GLB</a> · <a href="{v["references"][0]["url"]}">ESSR 來源</a></p></section>')
    page='<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>超音波六部位圖庫｜待醫師審閱</title><style>body{font-family:system-ui,sans-serif;margin:0;background:#071721;color:#e7f1f2;line-height:1.85}main{max-width:1200px;margin:auto;padding:32px 20px}h1{line-height:1.35}a{color:#9bdddf}img{display:block;width:100%;height:auto;border-radius:14px}section{padding-block:30px;border-bottom:1px solid #39525f}.notice{padding:20px;background:#302b22;color:#f4d7a5;border-radius:12px}nav{display:flex;gap:22px;flex-wrap:wrap}a:focus-visible{outline:3px solid #f5c784;outline-offset:4px}</style><main><h1>超音波：六部位立體解剖與探頭位置</h1><p class="notice">'+NOTICE+'每部位僅示範一個代表性視窗，沒有合成 B 模式影像。</p><nav>'+''.join(f'<a href="#{x["id"]}">{x["name"]}</a>' for x in manifest['items'])+'</nav>'+''.join(tiles)+'<footer><p>靜態頁不載入遠端腳本；網站互動版：<a href="/ultrasound-atlas/">/ultrasound-atlas/</a>。直接開啟本地檔案時，此站內路徑不適用。</p><p><a href="README.md">來源與使用限制</a> · <a href="manifest.json">SHA-256 索引</a></p></footer></main></html>'
    (out/'index.html').write_text(page,encoding='utf-8')
    docs=root/'website/docs/08-ultrasound-atlas.md';docs.parent.mkdir(parents=True,exist_ok=True)
    docs.write_text('# 超音波六部位系列：交付與審閱\n\n'+NOTICE+'\n\n## 交付\n\n6 張主圖卡（18 個格式檔）、12 個 GLB 變體、12 張 3D 海報、來源與雜湊索引。這是六個代表性視窗，不是 24 個建模視窗；24 項清單僅用於引導延伸閱讀。\n\n## 待完成的醫師審閱\n\n- 核對每一圖的骨性地標、肌腱附著、神經位置與編號引線。\n- 核對各部位的擺位、主視窗選擇、長短軸及探頭標記約定。\n- 檢查腕隧道 9 條屈肌腱、正中神經與支持帶的相對關係。\n- 確認髖關節囊的青色線條不被誤解為積液；確認膝與踝的範圍說明。\n- 以真實設備和正式教材核對，不以生成模型作為診斷參照。\n- 在另一次人工審閱提交中，記錄審閱者、日期、異動與通過範圍；本次 `reviewStatus` 保持 `needs-clinician-review`。\n\n## 維護\n\n生成來源為 `website/scripts/ultrasound-atlas/`；互動頁為 `/ultrasound-atlas/`；圖庫為 `website/public/medical-visuals/ultrasound/`。文章插入以 HTML 標記界定，重建只更新該區塊，不覆寫原有影片、课程或書籍資料。'.replace('课程','課程')+'\n\n原有其他 47 組模型與醫學圖庫不屬於本次修改範圍。CI 報告僅證明檔案和網頁檢查，不代表臨床審核通過。\n',encoding='utf-8')
    if integrate:
        # Keep the legacy root-level knee close-up from cropping this nested atlas.
        viewer=root/'website/src/scripts/medical-model.ts'
        if viewer.exists():
            code=viewer.read_text(encoding='utf-8')
            needle='(root.dataset.src || "").includes("/knee-")'
            if needle in code:
                code=code.replace(needle,'(root.dataset.src || "").startsWith("/medical-visuals/knee-")',1)
                viewer.write_text(code,encoding='utf-8')
        page_path=root/'website/src/pages/ultrasound-atlas.astro';page_path.parent.mkdir(parents=True,exist_ok=True)
        if page_path.exists() and '<!-- ultrasound-atlas:generated-page -->' not in page_path.read_text(encoding='utf-8'):raise ValueError('Refusing to overwrite a non-generated atlas page.')
        page_path.write_text(PAGE,encoding='utf-8')
        source=root/'website/src/content/articles/msk-ultrasound-self-study.md'
        if not source.exists():raise FileNotFoundError(source)
        replace_block(source,article_section(),anchor='## 影片資源')
        article=source.read_text(encoding='utf-8');date=re.search(r'^updatedDate: (\d{4}-\d{2}-\d{2})$',article,re.M)
        if date and date.group(1)<DATE:
            source.write_text(article[:date.start()]+'updatedDate: '+DATE+article[date.end():],encoding='utf-8')
        replace_block(root/'website_blog/posts/2023-04-blog-post_30.md',article_section(archive=True))
        parent=root/'website_blog/medical_3d_assets/README.md'
        # Earlier asset indexes may have been removed during repository migration.
        if not parent.exists():
            parent.parent.mkdir(parents=True,exist_ok=True)
            parent.write_text('# 醫學立體解說素材\n\n各系列的用途、來源與醫師審閱狀態請見各自的說明。\n',encoding='utf-8')
        replace_block(parent,'## 超音波六部位新系列\n\n[肩／肘／腕／髖／膝／踝圖卡與完整素材索引](ultrasound/README.md)\n\n新增六張立體圖卡，以及網站內十二個長短軸 GLB 變體。已嵌入超音波文章；全部保持「待醫師審閱」，未改動外部 Blogger 網站。')
