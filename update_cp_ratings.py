#!/usr/bin/env python3
import urllib.request
import re
import json
import os

def fetch_cf():
    url = "https://codeforces.com/api/user.info?handles=Sneaky_Typer"
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)
    res = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
    cf_rating = res["result"][0]["rating"]
    cf_max_rating = res["result"][0]["maxRating"]
    cf_rank = res["result"][0]["rank"].title()
    return cf_rank, cf_rating, cf_max_rating

def fetch_codechef():
    url = "https://www.codechef.com/users/scorzion"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    req = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(req).read().decode("utf-8")
    
    rating_match = re.search(r'class="rating-number"\s*>\s*(\d+)', html)
    highest_match = re.search(r'Highest Rating\s+(\d+)', html)
    
    cc_rating = int(rating_match.group(1)) if rating_match else 0
    cc_max = int(highest_match.group(1)) if highest_match else 0
    
    # Calculate stars
    cc_stars = 0
    if "class=\"rating-star\"" in html:
        star_block = html.split('class="rating-star"')[1].split('</div>')[0]
        cc_stars = len(re.findall(r'&#9733;', star_block))
        
    return cc_stars, cc_rating, cc_max

def fetch_atcoder():
    url = "https://atcoder.jp/users/Scorzion"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    req = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(req).read().decode("utf-8")
    
    rating_match = re.search(r'Rating</th><td>.*?<span class=[\'\"]user-\w+[\'\"]>(\d+)</span>', html)
    highest_match = re.search(r'Highest Rating</th><td>.*?<span class=[\'\"]user-\w+[\'\"]>(\d+)</span>', html)
    
    ac_rating = int(rating_match.group(1)) if rating_match else 0
    ac_max = int(highest_match.group(1)) if highest_match else 0
    
    def get_color(rating):
        if rating < 400: return "Gray"
        if rating < 800: return "Brown"
        if rating < 1200: return "Green"
        if rating < 1600: return "Cyan"
        if rating < 2000: return "Blue"
        if rating < 2400: return "Yellow"
        if rating < 2800: return "Orange"
        return "Red"
        
    return get_color(ac_rating), ac_rating, ac_max

def main():
    print("Fetching Codeforces ratings...")
    try:
        cf_rank, cf_rating, cf_max = fetch_cf()
        print(f"Codeforces: {cf_rank} ({cf_rating}, Max: {cf_max})")
    except Exception as e:
        print(f"Error fetching Codeforces: {e}")
        return

    print("Fetching CodeChef ratings...")
    try:
        cc_stars, cc_rating, cc_max = fetch_codechef()
        print(f"CodeChef: {cc_stars} Stars ({cc_rating}, Max: {cc_max})")
    except Exception as e:
        print(f"Error fetching CodeChef: {e}")
        return

    print("Fetching AtCoder ratings...")
    try:
        ac_color, ac_rating, ac_max = fetch_atcoder()
        print(f"AtCoder: {ac_color} ({ac_rating}, Max: {ac_max})")
    except Exception as e:
        print(f"Error fetching AtCoder: {e}")
        return

    svg_path = "cp_achievements.svg"
    if not os.path.exists(svg_path):
        print(f"File not found: {svg_path}")
        return

    with open(svg_path, "r", encoding="utf-8") as f:
        svg_content = f.read()

    # Regex replacements
    cf_pattern = r"(<!-- CF -->\s*<tspan class=\"bullet\"[^>]*>› </tspan>\s*<tspan class=\"bold-txt\">)[^<]*(</tspan> at Codeforces \()[^\)]*(\))"
    cf_replacement = rf"\g<1>{cf_rank}\g<2>Rating: {cf_rating}, Max: {cf_max}\g<3>"
    svg_content = re.sub(cf_pattern, cf_replacement, svg_content)

    cc_pattern = r"(<!-- CC -->\s*<tspan class=\"bullet\"[^>]*>› </tspan>\s*<tspan class=\"bold-txt\">)[^<]*(</tspan> at CodeChef \()[^\)]*(\))"
    cc_replacement = rf"\g<1>{cc_stars} Star\g<2>Rating: {cc_rating}, Max: {cc_max}\g<3>"
    svg_content = re.sub(cc_pattern, cc_replacement, svg_content)

    ac_pattern = r"(<!-- AC -->\s*<tspan class=\"bullet\"[^>]*>› </tspan>\s*<tspan class=\"bold-txt\">)[^<]*(</tspan> at AtCoder \()[^\)]*(\))"
    ac_replacement = rf"\g<1>{ac_color}\g<2>Rating: {ac_rating}, Max: {ac_max}\g<3>"
    svg_content = re.sub(ac_pattern, ac_replacement, svg_content)

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    
    print("Successfully updated cp_achievements.svg!")

if __name__ == "__main__":
    main()
