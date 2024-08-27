# YouTube to SRT Converter

This Cloudflare Worker converts YouTube video subtitles to SRT format.

## Setup

1. Install Node.js and npm if you haven't already.

2. Clone this repository:
   ```
   git clone https://github.com/your-username/youtube-to-srt-worker.git
   cd youtube-to-srt-worker
   ```

3. Install the dependencies:
   ```
   npm install
   ```

4. Install Wrangler CLI globally:
   ```
   npm install -g wrangler
   ```

5. Authenticate with Cloudflare:
   ```
   wrangler login
   ```

## Development

To run the worker locally for development:

```
wrangler dev
```

This will start a local server, typically at `http://localhost:8787`.

## Deployment

To deploy the worker to Cloudflare:

```
wrangler publish
```

## Usage

Once deployed, you can use the worker by sending a GET request with a YouTube URL as a query parameter:

```
https://your-worker-subdomain.workers.dev/?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

Replace `your-worker-subdomain` with the actual subdomain of your deployed worker, and the YouTube URL with the video you want to convert.

The response will be the SRT content as plain text.

## Project Structure

- `src/index.ts`: Main TypeScript file containing the worker logic
- `wrangler.toml`: Configuration file for Cloudflare Workers
- `package.json`: Node.js project file with dependencies and scripts
- `tsconfig.json`: TypeScript configuration file

## Dependencies

This project uses the following open source packages:

- [youtube-captions-scraper](https://github.com/algolia/youtube-captions-scraper): MIT License
- [@cloudflare/workers-types](https://github.com/cloudflare/workers-types): BSD-3-Clause License
- [typescript](https://github.com/microsoft/TypeScript): Apache-2.0 License
- [webpack](https://github.com/webpack/webpack): MIT License

For full license texts, please see the THIRD_PARTY_NOTICES.md file in this repository.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).