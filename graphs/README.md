# Autoware Analysis Graphs

This directory contains visualization graphs for the Autoware Contributors Analysis Report.

## Generated Images

The following PNG images are automatically generated from Graphviz DOT files:

1. **contributors_growth.png** - Timeline showing cumulative contributor growth from 2022 to 2025
2. **contributor_types.png** - Distribution of contributors by type (code vs community)
3. **tier4_impact.png** - Comparison of TIER IV engineers vs external contributors
4. **repo_activity.png** - Activity breakdown across different Autoware repositories
5. **star_growth.png** - GitHub star acquisition timeline from 2015 to 2025
6. **achievements.png** - Key achievements overview for the Autoware project

## Regenerating Images

To regenerate all images from the DOT source files:

```bash
# Navigate to the graphs directory
cd graphs/

# Generate all PNG images at once
for file in *.dot; do
    dot -Tpng "$file" -o "${file%.dot}.png"
done
```

Or generate individual images:

```bash
dot -Tpng contributors_growth.dot -o contributors_growth.png
dot -Tpng contributor_types.dot -o contributor_types.png
dot -Tpng tier4_impact.dot -o tier4_impact.png
dot -Tpng repo_activity.dot -o repo_activity.png
dot -Tpng star_growth.dot -o star_growth.png
dot -Tpng achievements.dot -o achievements.png
```

## Prerequisites

- **Graphviz** must be installed on your system
- Install on macOS: `brew install graphviz`
- Install on Ubuntu/Debian: `sudo apt-get install graphviz`
- Install on Windows: Download from https://graphviz.org/download/

## Modifying Graphs

To modify the appearance or data in the graphs:

1. Edit the corresponding `.dot` file in this directory
2. Regenerate the PNG image using the commands above
3. The updated image will automatically appear in ANALYSIS_REPORT.md

## Graph Format

All graphs are created using the DOT language from Graphviz. Key features:

- **Layout engines**: Uses `dot` (hierarchical layouts) for most graphs
- **Output format**: PNG at default resolution
- **Color schemes**: Uses standard Graphviz color names (lightblue, lightgreen, gold, etc.)
- **Node shapes**: Varies by graph (box, cylinder, star, ellipse)

## Troubleshooting

If images appear broken or don't render:

1. Check that the DOT file has valid syntax: `dot -Tpng filename.dot -o test.png`
2. Ensure Graphviz is properly installed: `which dot`
3. Verify file permissions: `ls -la *.png`
4. Check for error messages in the console output

## File Structure

```
graphs/
├── README.md                    # This file
├── contributors_growth.dot      # DOT source
├── contributors_growth.png      # Generated image
├── contributor_types.dot
├── contributor_types.png
├── tier4_impact.dot
├── tier4_impact.png
├── repo_activity.dot
├── repo_activity.png
├── star_growth.dot
├── star_growth.png
├── achievements.dot
└── achievements.png
```

## Integration with Analysis Report

These images are referenced in the main `ANALYSIS_REPORT.md` file using relative paths:

```markdown
![Description](graphs/filename.png)
```

When viewing the report on GitHub or in a markdown viewer, the images will be automatically embedded and displayed inline.

---

**Last Updated**: October 28, 2025
**Tool**: Graphviz
**Format**: DOT → PNG
