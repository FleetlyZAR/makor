import { defineConfig } from 'astro/config';

import cloudflare from "@astrojs/cloudflare";

// Set "site" to your final domain. It is used for canonical URLs and the sitemap.
export default defineConfig({
  site: 'https://www.makor.co.za',
  output: "hybrid",
  adapter: cloudflare()
});