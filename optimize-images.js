// optimize-images.js
// Usage: node optimize-images.js
// Requires: npm install sharp
// Scans all HTML files + custom.css for referenced images, then:
//   1. Re-encodes referenced WebP files >100KB at 85% quality (90% for LCP hero)
//   2. Lists PNG files safe to delete (unreferenced with WebP counterparts)
//   3. Flags large unreferenced files

const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const IMAGES_DIR = path.join(__dirname, 'images');
const LCP_IMAGE = 'lawn7.webp';
const SKIP_BELOW_KB = 100;

function getReferencedImages() {
  const referenced = new Set();

  // Scan all .html files in root directory
  const htmlFiles = fs.readdirSync(__dirname).filter(f => f.endsWith('.html'));
  for (const file of htmlFiles) {
    const content = fs.readFileSync(path.join(__dirname, file), 'utf8');
    // Match src="images/xxx", href="images/xxx", url(images/xxx), url("images/xxx")
    for (const m of content.matchAll(/(?:src|href|content|url)\s*[=\(]["']?images\/([^"'\s\)>?#]+)/g)) {
      referenced.add(m[1]);
    }
  }

  // Scan custom.css for background-image references (../images/xxx)
  try {
    const css = fs.readFileSync(path.join(__dirname, 'css', 'custom.css'), 'utf8');
    for (const m of css.matchAll(/url\(['"]?\.\.\/images\/([^'")\s]+)['"]?\)/g)) {
      referenced.add(m[1]);
    }
  } catch (e) {
    console.warn('Could not read css/custom.css:', e.message);
  }

  return referenced;
}

async function compressWebP(referenced) {
  const webpFiles = fs.readdirSync(IMAGES_DIR)
    .filter(f => f.toLowerCase().endsWith('.webp'))
    .sort();

  let totalSaved = 0;
  let compressed = 0;
  let skipped = 0;

  for (const file of webpFiles) {
    if (!referenced.has(file)) {
      continue; // Skip unreferenced files
    }

    const fp = path.join(IMAGES_DIR, file);
    const stat = fs.statSync(fp);

    if (stat.size < SKIP_BELOW_KB * 1024) {
      console.log(`SKIP  (${(stat.size/1024).toFixed(0).padStart(5)}KB) ${file}`);
      skipped++;
      continue;
    }

    const quality = file === LCP_IMAGE ? 90 : 85;
    const tmp = fp + '.tmp.webp';

    try {
      await sharp(fp)
        .webp({ quality, effort: 6 })
        .toFile(tmp);

      const newStat = fs.statSync(tmp);
      const saved = stat.size - newStat.size;
      const pct = ((saved / stat.size) * 100).toFixed(1);

      console.log(`COMPRESS (${(stat.size/1024).toFixed(0).padStart(5)}KB → ${(newStat.size/1024).toFixed(0).padStart(5)}KB, -${pct}%, q=${quality}) ${file}`);

      fs.renameSync(tmp, fp);
      totalSaved += saved;
      compressed++;
    } catch (e) {
      console.error(`ERROR: ${file}: ${e.message}`);
      if (fs.existsSync(tmp)) fs.unlinkSync(tmp);
    }
  }

  console.log(`\nCompressed ${compressed} files. Skipped ${skipped} (under ${SKIP_BELOW_KB}KB).`);
  console.log(`Total savings: ${(totalSaved / 1024 / 1024).toFixed(2)}MB`);
}

function listDeletablePNGs(referenced) {
  console.log('\n=== PNG FILES SAFE TO DELETE ===');
  const pngFiles = fs.readdirSync(IMAGES_DIR).filter(f => f.toLowerCase().endsWith('.png')).sort();
  let totalSize = 0;

  for (const file of pngFiles) {
    const webp = file.replace(/\.png$/i, '.webp');
    const webpPath = path.join(IMAGES_DIR, webp);
    const pngReferenced = referenced.has(file);
    const webpExists = fs.existsSync(webpPath);
    const webpReferenced = referenced.has(webp);

    if (!pngReferenced) {
      const size = fs.statSync(path.join(IMAGES_DIR, file)).size;
      totalSize += size;
      const reason = webpExists && webpReferenced
        ? '(WebP counterpart referenced)'
        : webpExists
          ? '(WebP exists but also unreferenced)'
          : '(no WebP counterpart, unreferenced)';
      console.log(`DELETE: images/${file} (${(size/1024/1024).toFixed(1)}MB) ${reason}`);
    }
  }

  console.log(`\nTotal PNG deletion savings: ${(totalSize / 1024 / 1024).toFixed(1)}MB`);
}

function listJunkFiles(referenced) {
  console.log('\n=== OTHER JUNK/LARGE UNREFERENCED FILES ===');
  const allFiles = fs.readdirSync(IMAGES_DIR);

  for (const file of allFiles) {
    // Flag large unreferenced non-image files
    const ext = path.extname(file).toLowerCase();
    if (['.psd', '.ini', '.mp4'].includes(ext) || file.includes(' - Copy') || file.includes(' copy')) {
      const size = fs.statSync(path.join(IMAGES_DIR, file)).size;
      console.log(`JUNK: images/${file} (${(size/1024).toFixed(0)}KB)`);
    }
    // Flag large unreferenced SVGs
    if (ext === '.svg' && !referenced.has(file)) {
      const size = fs.statSync(path.join(IMAGES_DIR, file)).size;
      if (size > 50 * 1024) {
        console.log(`LARGE UNREFERENCED SVG: images/${file} (${(size/1024).toFixed(0)}KB)`);
      }
    }
  }
}

(async () => {
  console.log('=== No-BS Yardwork Image Optimizer ===\n');
  console.log('Scanning HTML files and CSS for referenced images...');
  const referenced = getReferencedImages();
  console.log(`Found ${referenced.size} unique referenced images.\n`);

  console.log('=== COMPRESSING REFERENCED WebP FILES ===');
  await compressWebP(referenced);

  listDeletablePNGs(referenced);
  listJunkFiles(referenced);

  console.log('\n=== DONE ===');
})();
