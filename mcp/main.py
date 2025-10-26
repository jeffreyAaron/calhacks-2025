import os
import argparse
from bom_parser import BOMParser
from website_finder import WebsiteFinder
from browser_controller import BrowserController
from csv_updater import CSVUpdater


def main():
    parser = argparse.ArgumentParser(description='automated bom part ordering system')
    parser.add_argument('csv_file', type=str, help='path to the bom csv file')
    parser.add_argument('--num-websites', type=int, default=3, help='number of websites to search per part')
    parser.add_argument('--output', type=str, default=None, help='output csv file path')
    parser.add_argument('--gemini-key', type=str, default=None, help='gemini api key')
    parser.add_argument('--openai-key', type=str, default=None, help='openai api key')
    parser.add_argument('--use-open-source', action='store_true', help='use open source model instead of openai')
    parser.add_argument('--model-name', type=str, default=None, help='model name (e.g., llama3.1, gpt-4)')
    parser.add_argument('--base-url', type=str, default=None, help='base url for model api (e.g., http://localhost:11434/v1)')
    parser.add_argument('--headless', action='store_true', help='run browser in headless mode (invisible, faster)')
    parser.add_argument('--show-browser', action='store_true', help='show browser window (opposite of headless)')
    parser.add_argument('--no-browser', action='store_true', help='use llm simulation instead of real browser')
    
    args = parser.parse_args()
    
    # determine headless mode
    headless = args.headless and not args.show_browser
    
    print("=== bom automated ordering system ===\n")
    
    # step 1: parse the bom csv
    print("step 1: parsing bom csv...")
    bom_parser = BOMParser(args.csv_file)
    parts = bom_parser.get_parts()
    part_names = bom_parser.get_part_names()
    print(f"found {len(part_names)} parts in bom\n")
    
    # step 2: find relevant websites using gemini
    print("step 2: finding relevant websites using gemini...")
    website_finder = WebsiteFinder(
        api_key=args.gemini_key,
        num_websites=args.num_websites
    )
    websites_map = website_finder.find_websites_for_parts(part_names)
    print(f"found websites for all parts\n")
    
    # step 3: use browser automation to search and add to cart
    browser_mode = "headless" if headless else "visible"
    automation_type = "llm simulation" if args.no_browser else f"real browser ({browser_mode})"
    print(f"step 3: searching parts on websites using {automation_type}...")
    
    if not args.no_browser and headless:
        print("⚠️  note: headless mode may trigger cloudflare/bot detection on digikey/mouser")
        print("   consider using --show-browser for better success rate")
        print()
    
    browser_controller = BrowserController(
        api_key=args.openai_key,
        use_open_source=args.use_open_source,
        model_name=args.model_name,
        base_url=args.base_url,
        use_real_browser=not args.no_browser,
        headless=headless
    )
    
    all_results = {}
    for part_name in part_names:
        print(f"\nprocessing: {part_name}")
        websites = websites_map.get(part_name, [])
        if websites:
            results = browser_controller.process_part_across_websites(part_name, websites)
            all_results[part_name] = results
        else:
            print(f"  no websites found for {part_name}")
            all_results[part_name] = []
    
    print("\n")
    
    # step 4: append results to original csv
    print("step 4: updating csv with results...")
    csv_updater = CSVUpdater(args.csv_file, args.output)
    output_path = csv_updater.append_results_to_csv(parts, all_results)
    
    print(f"\n=== process complete ===")
    print(f"results saved to: {output_path}")
    

if __name__ == "__main__":
    main()

