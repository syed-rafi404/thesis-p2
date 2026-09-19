"""
Thesis Figures Generator
Multimodal Banglish Classroom Summarizer
Generates publication-quality figures for Chapters 5 and 6
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# Set publication-quality defaults
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.grid': True,
    'grid.alpha': 0.3,
})

# Create output directory
OUTPUT_DIR = r"c:\Users\T2520785\thesisP2\P2\figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================================
# DATA FROM THESIS RESULTS
# ============================================================================

# Dataset information (Table 5.X - BanglaASR Dataset)
VIDEOS = {
    'BanglaASR1': {'topic': 'Python Variables', 'domain': 'Python', 'gt_chars': 8124, 'keywords': 45},
    'BanglaASR2': {'topic': 'Python Input', 'domain': 'Python', 'gt_chars': 6484, 'keywords': 38},
    'BanglaASR3': {'topic': 'Python Conditionals', 'domain': 'Python', 'gt_chars': 16558, 'keywords': 67},
    'BanglaASR4': {'topic': 'Python Loops', 'domain': 'Python', 'gt_chars': 7892, 'keywords': 42},
    'BanglaASR5': {'topic': 'Lists/Tuples/Arrays', 'domain': 'Python', 'gt_chars': 15272, 'keywords': 58},
    'BanglaASR6': {'topic': 'DLD Gates', 'domain': 'DLD', 'gt_chars': 5234, 'keywords': 35},
    'BanglaASR7': {'topic': 'Universal Gates', 'domain': 'DLD', 'gt_chars': 4876, 'keywords': 32},
    'BanglaASR8': {'topic': 'DBMS Introduction', 'domain': 'DBMS', 'gt_chars': 4523, 'keywords': 28},
    'BanglaASR9': {'topic': 'SQL SELECT', 'domain': 'DBMS', 'gt_chars': 4178, 'keywords': 31},
}

# Per-video results (Table 6.X)
RESULTS = {
    'BanglaASR1': {'f1': 70.5, 'precision': 81.6, 'recall': 62.0, 'fuzzy': 43.1},
    'BanglaASR2': {'f1': 75.8, 'precision': 84.7, 'recall': 68.7, 'fuzzy': 45.5},
    'BanglaASR3': {'f1': 79.6, 'precision': 88.2, 'recall': 72.6, 'fuzzy': 47.0},
    'BanglaASR4': {'f1': 62.4, 'precision': 78.7, 'recall': 51.7, 'fuzzy': 45.8},
    'BanglaASR5': {'f1': 73.2, 'precision': 87.3, 'recall': 63.0, 'fuzzy': 44.0},
    'BanglaASR6': {'f1': 70.8, 'precision': 86.4, 'recall': 60.0, 'fuzzy': 45.6},
    'BanglaASR7': {'f1': 75.0, 'precision': 82.8, 'recall': 68.6, 'fuzzy': 46.1},
    'BanglaASR8': {'f1': 78.7, 'precision': 80.6, 'recall': 76.9, 'fuzzy': 42.8},
    'BanglaASR9': {'f1': 78.6, 'precision': 82.1, 'recall': 75.4, 'fuzzy': 43.4},
}

# Domain results
DOMAIN_RESULTS = {
    'Python': {'f1': 72.3, 'precision': 84.1, 'recall': 63.6, 'videos': 5},
    'DLD': {'f1': 72.9, 'precision': 84.6, 'recall': 64.3, 'videos': 2},
    'DBMS': {'f1': 78.7, 'precision': 81.4, 'recall': 76.2, 'videos': 2},
}

# Ablation results
ABLATION = {
    'Whisper-Only': {'f1': 68.2, 'precision': 76.4, 'recall': 61.8},
    'Whisper + Cleaning': {'f1': 71.5, 'precision': 82.1, 'recall': 63.2},
    'Visual-Only': {'f1': 42.3, 'precision': 89.2, 'recall': 28.4},
    'Full Pipeline': {'f1': 73.9, 'precision': 83.6, 'recall': 66.5},
}

# Visual bias experiment
VISUAL_BIAS = {
    'No Bias': {'f1': 68.2, 'precision': 76.4, 'recall': 61.8},
    'Light (α=0.1)': {'f1': 69.8, 'precision': 74.2, 'recall': 66.1},
    'Medium (α=0.3)': {'f1': 67.1, 'precision': 68.5, 'recall': 65.8},
    'Heavy (α=0.5)': {'f1': 58.4, 'precision': 55.2, 'recall': 62.1},
    'Verification': {'f1': 73.9, 'precision': 83.6, 'recall': 66.5},
}

# Failure modes
FAILURE_MODES = {
    'Phonetic Approximation': 35,
    'Technical Term Confusion': 25,
    'Repetition Hallucination': 18,
    'Visual Extraction Error': 12,
    'Alignment Mismatch': 10,
}

# Color schemes
DOMAIN_COLORS = {'Python': '#3776AB', 'DLD': '#E74C3C', 'DBMS': '#27AE60'}
METRIC_COLORS = {'f1': '#2E86AB', 'precision': '#A23B72', 'recall': '#F18F01'}


# ============================================================================
# FIGURE 5.7: Dataset Distribution
# ============================================================================
def create_dataset_distribution():
    """Create Figure 5.7: Dataset distribution (domain pie + character bar)"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Panel A: Domain Distribution Pie Chart
    domain_chars = {}
    domain_videos = {}
    for vid, info in VIDEOS.items():
        domain = info['domain']
        domain_chars[domain] = domain_chars.get(domain, 0) + info['gt_chars']
        domain_videos[domain] = domain_videos.get(domain, 0) + 1
    
    domains = list(domain_chars.keys())
    chars = [domain_chars[d] for d in domains]
    colors = [DOMAIN_COLORS[d] for d in domains]
    
    wedges, texts, autotexts = ax1.pie(
        chars, 
        labels=[f"{d}\n({domain_videos[d]} videos)" for d in domains],
        autopct=lambda pct: f'{pct:.1f}%',
        colors=colors,
        explode=(0.02, 0.02, 0.02),
        shadow=False,
        startangle=90,
        textprops={'fontsize': 11}
    )
    ax1.set_title('(a) Domain Distribution by Character Count', fontweight='bold', pad=15)
    
    # Panel B: Character Count Bar Chart
    videos_sorted = sorted(VIDEOS.items(), key=lambda x: x[1]['gt_chars'], reverse=True)
    video_names = [v[0].replace('BanglaASR', 'ASR') for v in videos_sorted]
    char_counts = [v[1]['gt_chars'] / 1000 for v in videos_sorted]  # Convert to thousands
    bar_colors = [DOMAIN_COLORS[v[1]['domain']] for v in videos_sorted]
    
    bars = ax2.barh(video_names, char_counts, color=bar_colors, edgecolor='black', linewidth=0.5)
    ax2.set_xlabel('Ground Truth Characters (thousands)', fontweight='bold')
    ax2.set_ylabel('Video ID', fontweight='bold')
    ax2.set_title('(b) Ground Truth Size by Video', fontweight='bold', pad=15)
    ax2.invert_yaxis()
    
    # Add value labels
    for bar, val in zip(bars, char_counts):
        ax2.text(val + 0.3, bar.get_y() + bar.get_height()/2, 
                f'{val:.1f}k', va='center', fontsize=9)
    
    # Legend
    legend_patches = [mpatches.Patch(color=DOMAIN_COLORS[d], label=d) for d in domains]
    ax2.legend(handles=legend_patches, loc='lower right', title='Domain')
    
    ax2.set_xlim(0, max(char_counts) * 1.15)
    ax2.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_5_7_dataset_distribution.png'))
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_5_7_dataset_distribution.pdf'))
    print("✓ Figure 5.7: Dataset Distribution saved")
    plt.close()


# ============================================================================
# FIGURE 6.1: Per-Video Performance Bar Chart
# ============================================================================
def create_per_video_performance():
    """Create Figure 6.1: Per-video Term F1 performance"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Sort by F1 score
    sorted_results = sorted(RESULTS.items(), key=lambda x: x[1]['f1'], reverse=True)
    video_names = [v[0].replace('BanglaASR', 'ASR') + '\n' + VIDEOS[v[0]]['topic'][:15] 
                   for v in sorted_results]
    f1_scores = [v[1]['f1'] for v in sorted_results]
    bar_colors = [DOMAIN_COLORS[VIDEOS[v[0]]['domain']] for v in sorted_results]
    
    x = np.arange(len(video_names))
    bars = ax.bar(x, f1_scores, color=bar_colors, edgecolor='black', linewidth=0.5, width=0.7)
    
    # Add value labels on bars
    for bar, val in zip(bars, f1_scores):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
               f'{val:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Mean line
    mean_f1 = np.mean(f1_scores)
    ax.axhline(y=mean_f1, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_f1:.1f}%')
    
    ax.set_xlabel('Video', fontweight='bold')
    ax.set_ylabel('Term F1 Score (%)', fontweight='bold')
    ax.set_title('Per-Video Term F1 Performance (Ordered by Score)', fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(video_names, fontsize=9)
    ax.set_ylim(0, 90)
    
    # Legend
    legend_patches = [mpatches.Patch(color=DOMAIN_COLORS[d], label=d) for d in DOMAIN_COLORS]
    legend_patches.append(plt.Line2D([0], [0], color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_f1:.1f}%'))
    ax.legend(handles=legend_patches, loc='lower left')
    
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_6_1_per_video_f1.png'))
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_6_1_per_video_f1.pdf'))
    print("✓ Figure 6.1: Per-Video Performance saved")
    plt.close()


# ============================================================================
# FIGURE 6.2: Precision-Recall Scatter Plot
# ============================================================================
def create_precision_recall_scatter():
    """Create Figure 6.2: Precision vs Recall scatter plot"""
    fig, ax = plt.subplots(figsize=(9, 7))
    
    for vid, res in RESULTS.items():
        domain = VIDEOS[vid]['domain']
        color = DOMAIN_COLORS[domain]
        ax.scatter(res['recall'], res['precision'], 
                  c=color, s=150, edgecolors='black', linewidths=1, zorder=3)
        # Label each point
        ax.annotate(vid.replace('BanglaASR', 'ASR'), 
                   (res['recall'], res['precision']),
                   xytext=(5, 5), textcoords='offset points', fontsize=9)
    
    # Add iso-F1 curves
    for f1 in [0.5, 0.6, 0.7, 0.8]:
        recall_range = np.linspace(0.01, 1, 100)
        precision_range = (f1 * recall_range) / (2 * recall_range - f1)
        valid = (precision_range > 0) & (precision_range <= 1)
        ax.plot(recall_range[valid] * 100, precision_range[valid] * 100, 
               '--', color='gray', alpha=0.5, linewidth=1)
        # Label the curve
        idx = np.argmin(np.abs(recall_range[valid] - 0.5))
        if idx < len(recall_range[valid]):
            ax.text(recall_range[valid][idx] * 100 + 1, precision_range[valid][idx] * 100,
                   f'F1={f1}', fontsize=8, color='gray')
    
    # Mean point
    mean_prec = np.mean([r['precision'] for r in RESULTS.values()])
    mean_rec = np.mean([r['recall'] for r in RESULTS.values()])
    ax.scatter(mean_rec, mean_prec, c='red', s=200, marker='*', 
              edgecolors='black', linewidths=1, zorder=4, label=f'Mean ({mean_rec:.1f}%, {mean_prec:.1f}%)')
    
    ax.set_xlabel('Term Recall (%)', fontweight='bold')
    ax.set_ylabel('Term Precision (%)', fontweight='bold')
    ax.set_title('Precision-Recall Trade-off by Video', fontweight='bold', pad=15)
    ax.set_xlim(45, 85)
    ax.set_ylim(70, 95)
    
    # Legend
    legend_patches = [mpatches.Patch(color=DOMAIN_COLORS[d], label=d) for d in DOMAIN_COLORS]
    legend_patches.append(plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='red',
                                     markersize=15, label='Mean'))
    ax.legend(handles=legend_patches, loc='lower left')
    
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_6_2_precision_recall.png'))
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_6_2_precision_recall.pdf'))
    print("✓ Figure 6.2: Precision-Recall Scatter saved")
    plt.close()


# ============================================================================
# FIGURE 6.3: Domain Performance Comparison
# ============================================================================
def create_domain_comparison():
    """Create Figure 6.3: Performance by technical domain"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    domains = list(DOMAIN_RESULTS.keys())
    x = np.arange(len(domains))
    width = 0.25
    
    f1_vals = [DOMAIN_RESULTS[d]['f1'] for d in domains]
    prec_vals = [DOMAIN_RESULTS[d]['precision'] for d in domains]
    rec_vals = [DOMAIN_RESULTS[d]['recall'] for d in domains]
    
    bars1 = ax.bar(x - width, f1_vals, width, label='Term F1', color=METRIC_COLORS['f1'], edgecolor='black')
    bars2 = ax.bar(x, prec_vals, width, label='Precision', color=METRIC_COLORS['precision'], edgecolor='black')
    bars3 = ax.bar(x + width, rec_vals, width, label='Recall', color=METRIC_COLORS['recall'], edgecolor='black')
    
    # Add value labels
    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                   f'{height:.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    add_labels(bars1)
    add_labels(bars2)
    add_labels(bars3)
    
    ax.set_xlabel('Technical Domain', fontweight='bold')
    ax.set_ylabel('Score (%)', fontweight='bold')
    ax.set_title('Performance Metrics by Technical Domain', fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{d}\n({DOMAIN_RESULTS[d]['videos']} videos)" for d in domains])
    ax.set_ylim(0, 100)
    ax.legend(loc='upper right')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_6_3_domain_comparison.png'))
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_6_3_domain_comparison.pdf'))
    print("✓ Figure 6.3: Domain Comparison saved")
    plt.close()


# ============================================================================
# FIGURE 6.4: Ablation Study Results
# ============================================================================
def create_ablation_study():
    """Create Figure 6.4: Ablation study results"""
    fig, ax = plt.subplots(figsize=(11, 6))
    
    configs = list(ABLATION.keys())
    x = np.arange(len(configs))
    width = 0.25
    
    f1_vals = [ABLATION[c]['f1'] for c in configs]
    prec_vals = [ABLATION[c]['precision'] for c in configs]
    rec_vals = [ABLATION[c]['recall'] for c in configs]
    
    bars1 = ax.bar(x - width, f1_vals, width, label='Term F1', color=METRIC_COLORS['f1'], edgecolor='black')
    bars2 = ax.bar(x, prec_vals, width, label='Precision', color=METRIC_COLORS['precision'], edgecolor='black')
    bars3 = ax.bar(x + width, rec_vals, width, label='Recall', color=METRIC_COLORS['recall'], edgecolor='black')
    
    # Highlight the full pipeline
    for bar in [bars1[-1], bars2[-1], bars3[-1]]:
        bar.set_edgecolor('green')
        bar.set_linewidth(3)
    
    # Add value labels
    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                   f'{height:.1f}', ha='center', va='bottom', fontsize=9)
    
    add_labels(bars1)
    add_labels(bars2)
    add_labels(bars3)
    
    # Add delta annotations for F1
    baseline_f1 = ABLATION['Whisper-Only']['f1']
    for i, (config, vals) in enumerate(ABLATION.items()):
        if config != 'Whisper-Only':
            delta = vals['f1'] - baseline_f1
            color = 'green' if delta > 0 else 'red'
            ax.annotate(f'{delta:+.1f}%', 
                       xy=(i - width, vals['f1'] + 3),
                       ha='center', fontsize=8, color=color, fontweight='bold')
    
    ax.set_xlabel('Configuration', fontweight='bold')
    ax.set_ylabel('Score (%)', fontweight='bold')
    ax.set_title('Ablation Study: Component Contributions', fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(configs, fontsize=10)
    ax.set_ylim(0, 100)
    ax.legend(loc='upper right')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_6_4_ablation_study.png'))
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_6_4_ablation_study.pdf'))
    print("✓ Figure 6.4: Ablation Study saved")
    plt.close()


# ============================================================================
# FIGURE 6.5: Failure Mode Distribution
# ============================================================================
def create_failure_mode_pie():
    """Create Figure 6.5: Failure mode distribution"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    labels = list(FAILURE_MODES.keys())
    sizes = list(FAILURE_MODES.values())
    colors = ['#E74C3C', '#F39C12', '#9B59B6', '#3498DB', '#1ABC9C']
    explode = (0.05, 0.02, 0.02, 0.02, 0.02)
    
    wedges, texts, autotexts = ax.pie(
        sizes, 
        labels=labels,
        autopct=lambda pct: f'{pct:.0f}%\n({int(pct/100*sum(sizes))})',
        colors=colors,
        explode=explode,
        shadow=False,
        startangle=140,
        textprops={'fontsize': 11},
        pctdistance=0.75
    )
    
    # Make percentage text bold
    for autotext in autotexts:
        autotext.set_fontweight('bold')
    
    ax.set_title('Distribution of Failure Modes in System Output', fontweight='bold', pad=20, fontsize=14)
    
    # Add a text box with additional info
    textstr = 'Total Errors Analyzed: 100%\nDominant Mode: Phonetic Approximation'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.02, 0.02, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='bottom', bbox=props)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_6_5_failure_modes.png'))
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_6_5_failure_modes.pdf'))
    print("✓ Figure 6.5: Failure Mode Distribution saved")
    plt.close()


# ============================================================================
# FIGURE 6.6: Visual Bias Intensity vs Performance
# ============================================================================
def create_visual_bias_line():
    """Create Figure 6.6: Visual bias intensity effect on performance"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    configs = list(VISUAL_BIAS.keys())
    x = np.arange(len(configs))
    
    f1_vals = [VISUAL_BIAS[c]['f1'] for c in configs]
    prec_vals = [VISUAL_BIAS[c]['precision'] for c in configs]
    rec_vals = [VISUAL_BIAS[c]['recall'] for c in configs]
    
    # Plot lines with markers
    ax.plot(x, f1_vals, 'o-', color=METRIC_COLORS['f1'], linewidth=2.5, 
            markersize=10, label='Term F1', markeredgecolor='black')
    ax.plot(x, prec_vals, 's-', color=METRIC_COLORS['precision'], linewidth=2.5, 
            markersize=10, label='Precision', markeredgecolor='black')
    ax.plot(x, rec_vals, '^-', color=METRIC_COLORS['recall'], linewidth=2.5, 
            markersize=10, label='Recall', markeredgecolor='black')
    
    # Highlight the verification-based approach
    ax.axvline(x=4, color='green', linestyle='--', linewidth=2, alpha=0.7)
    ax.annotate('Our Approach\n(Verification)', xy=(4, 75), xytext=(4.2, 80),
               fontsize=10, fontweight='bold', color='green',
               arrowprops=dict(arrowstyle='->', color='green'))
    
    # Shade the "harmful" region
    ax.axvspan(1.5, 3.5, alpha=0.1, color='red', label='Bias harms performance')
    
    # Add value labels
    for i, (f1, prec, rec) in enumerate(zip(f1_vals, prec_vals, rec_vals)):
        ax.text(i, f1 + 2, f'{f1:.1f}', ha='center', fontsize=9, color=METRIC_COLORS['f1'])
    
    ax.set_xlabel('Visual Bias Configuration', fontweight='bold')
    ax.set_ylabel('Score (%)', fontweight='bold')
    ax.set_title('Effect of Visual Bias Intensity on Performance', fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(configs, fontsize=10)
    ax.set_ylim(45, 95)
    ax.legend(loc='lower left')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_6_6_visual_bias.png'))
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_6_6_visual_bias.pdf'))
    print("✓ Figure 6.6: Visual Bias Effect saved")
    plt.close()


# ============================================================================
# BONUS: Combined Summary Figure
# ============================================================================
def create_summary_figure():
    """Create a summary figure combining key results"""
    fig = plt.figure(figsize=(14, 10))
    
    # Create grid
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    # Panel A: Overall metrics (gauge-like)
    ax1 = fig.add_subplot(gs[0, 0])
    metrics = {'Term F1': 73.9, 'Precision': 83.6, 'Recall': 66.5}
    colors = [METRIC_COLORS['f1'], METRIC_COLORS['precision'], METRIC_COLORS['recall']]
    bars = ax1.barh(list(metrics.keys()), list(metrics.values()), color=colors, edgecolor='black')
    ax1.set_xlim(0, 100)
    ax1.set_xlabel('Score (%)', fontweight='bold')
    ax1.set_title('(a) Overall System Performance', fontweight='bold')
    for bar, val in zip(bars, metrics.values()):
        ax1.text(val + 1, bar.get_y() + bar.get_height()/2, f'{val}%', va='center', fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    # Panel B: Domain comparison
    ax2 = fig.add_subplot(gs[0, 1])
    domains = list(DOMAIN_RESULTS.keys())
    f1_vals = [DOMAIN_RESULTS[d]['f1'] for d in domains]
    domain_colors = [DOMAIN_COLORS[d] for d in domains]
    bars = ax2.bar(domains, f1_vals, color=domain_colors, edgecolor='black')
    ax2.axhline(y=73.9, color='red', linestyle='--', label='Overall Mean')
    ax2.set_ylabel('Term F1 (%)', fontweight='bold')
    ax2.set_title('(b) Performance by Domain', fontweight='bold')
    ax2.set_ylim(0, 90)
    for bar, val in zip(bars, f1_vals):
        ax2.text(bar.get_x() + bar.get_width()/2, val + 1, f'{val:.1f}%', ha='center', fontweight='bold')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    # Panel C: Improvement over baseline
    ax3 = fig.add_subplot(gs[1, 0])
    configs = ['Baseline\n(Whisper)', '+ Cleaning', '+ Fusion\n(Full)']
    f1_vals = [68.2, 71.5, 73.9]
    improvements = [0, 3.3, 5.7]
    bars = ax3.bar(configs, f1_vals, color=['#95a5a6', '#3498db', '#27ae60'], edgecolor='black')
    ax3.set_ylabel('Term F1 (%)', fontweight='bold')
    ax3.set_title('(c) Cumulative Improvement', fontweight='bold')
    ax3.set_ylim(0, 85)
    for bar, val, imp in zip(bars, f1_vals, improvements):
        ax3.text(bar.get_x() + bar.get_width()/2, val + 1, f'{val}%', ha='center', fontweight='bold')
        if imp > 0:
            ax3.text(bar.get_x() + bar.get_width()/2, val - 5, f'+{imp}%', ha='center', color='white', fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)
    
    # Panel D: Statistical significance
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.text(0.5, 0.7, 'Statistical Significance', ha='center', va='center', 
            fontsize=16, fontweight='bold', transform=ax4.transAxes)
    ax4.text(0.5, 0.5, 'p = 0.003 **', ha='center', va='center', 
            fontsize=24, fontweight='bold', color='green', transform=ax4.transAxes)
    ax4.text(0.5, 0.3, "Cohen's d = 0.96 (Large Effect)", ha='center', va='center', 
            fontsize=14, transform=ax4.transAxes)
    ax4.text(0.5, 0.15, 'Improvement: +5.7% Term F1', ha='center', va='center', 
            fontsize=12, style='italic', transform=ax4.transAxes)
    ax4.set_xlim(0, 1)
    ax4.set_ylim(0, 1)
    ax4.axis('off')
    ax4.set_title('(d) Statistical Analysis', fontweight='bold')
    
    # Add border
    rect = plt.Rectangle((0.02, 0.02), 0.96, 0.96, fill=False, edgecolor='gray', linewidth=2, transform=ax4.transAxes)
    ax4.add_patch(rect)
    
    plt.suptitle('Multimodal Banglish Classroom Summarizer: Key Results', 
                fontsize=16, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_summary_results.png'))
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_summary_results.pdf'))
    print("✓ Summary Figure saved")
    plt.close()


# ============================================================================
# MAIN
# ============================================================================
def main():
    print("=" * 60)
    print("Generating Thesis Figures")
    print("=" * 60)
    print(f"Output directory: {OUTPUT_DIR}\n")
    
    # Generate all figures
    create_dataset_distribution()      # Figure 5.7
    create_per_video_performance()     # Figure 6.1
    create_precision_recall_scatter()  # Figure 6.2
    create_domain_comparison()         # Figure 6.3
    create_ablation_study()            # Figure 6.4
    create_failure_mode_pie()          # Figure 6.5
    create_visual_bias_line()          # Figure 6.6
    create_summary_figure()            # Bonus summary
    
    print("\n" + "=" * 60)
    print("All figures generated successfully!")
    print(f"Files saved to: {OUTPUT_DIR}")
    print("=" * 60)
    print("\nGenerated files:")
    for f in os.listdir(OUTPUT_DIR):
        if f.endswith(('.png', '.pdf')):
            print(f"  • {f}")


if __name__ == "__main__":
    main()
