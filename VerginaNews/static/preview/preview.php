<link rel="stylesheet" type="text/css" href="preview/preview.css">

<div id="preview_panel" class="hide-panel">
	<a href="javascript:;" class="preview-handler">
		<img src="preview/icon.png" alt="preview icon">
		<span>One Click Demo</span>
	</a>

	<span class="preview-line"></span>

	<div class="preview-viewport"></div>

	<div class="preview-wrap">
		<div class="preview-entry">
			<h3>The next generation of Magazine design.</h3>

			<p class="text-center pv4 mv1 mvt0">
				<a href="https://themeforest.net/item/tana-magazine-news-entertainment-fashion-template/16207440?ref=themeton" class="btn-link">Purchase Tana</a>
			</p>

			<h4>Main Concepts</h4>
			<br>

			<div class="c-item pw-hover-item" data-img="preview/images/main-1.jpg">
				<a href="index.php">
					<img src="preview/images/c1.png" align="concept">
				</a>
				<h5>News Politics</h5>
			</div>
			<div class="c-item pw-hover-item" data-img="preview/images/main-2.jpg">
				<a href="entertainment.php">
					<img src="preview/images/c2.png" align="concept">
				</a>
				<h5>Entertainment - Movie</h5>
			</div>
			<div class="c-item pw-hover-item" data-img="preview/images/music-preview.jpg">
				<a href="music.php">
					<img src="preview/images/music.jpg" align="concept">
				</a>
				<h5>Entertainment - Music</h5>
			</div>
			<div class="c-item pw-hover-item" data-img="preview/images/main-fashion.jpg">
				<a href="fashion.php">
					<img src="preview/images/thumb-fashion.jpg" align="concept">
				</a>
				<h5>Fashion Blog</h5>
			</div>
			<div class="c-item pw-hover-item" data-img="preview/images/main-3.jpg">
				<a href="blog.php">
					<img src="preview/images/c3.png" align="concept">
				</a>
				<h5>Personal Blog</h5>
			</div>
			<div class="c-item pw-hover-item" data-img="preview/images/main-travel.jpg">
				<a href="travel.php">
					<img src="preview/images/thumb-travel.jpg" align="concept">
				</a>
				<h5>Travel Agency</h5>
			</div>
			<div class="c-item pw-hover-item" data-img="preview/images/main-fitness.jpg">
				<a href="fitness.php">
					<img src="preview/images/thumb-fitness.jpg" align="concept">
				</a>
				<h5>Fitness Training</h5>
			</div>
			
			<br>
			<h4>Other Concepts</h4>
			<br>

			<div class="pw-row">
				<div class="pw-col">
					<a href="single.php" class="pw-hover-item" data-img="preview/images/single-1.jpg">
						<img src="preview/images/s1.png" alt="demo">
						<span>Single 1</span>
					</a>
				</div>
				<div class="pw-col">
					<a href="single-news.php" class="pw-hover-item" data-img="preview/images/single-2.jpg">
						<img src="preview/images/s2.png" alt="demo">
						<span>Single 2</span>
					</a>
				</div>
				<?php for($i=1; $i<=10; $i++): ?>
				<div class="pw-col">
					<a href="<?php echo $i==1 ? 'index.php' : "news$i.php"; ?>" class="pw-hover-item" data-img="preview/images/c<?php echo $i; ?>.jpg">
						<img src="preview/images/b<?php echo $i; ?>.png" alt="demo">
						<span>Concept <?php echo $i; ?></span>
					</a>
				</div>
				<?php endfor; ?>
				<div class="clearfix"></div>
			</div>

			<br>
			<p class="text-center">
				<a href="https://themeforest.net/item/tana-magazine-news-entertainment-fashion-template/16207440?ref=themeton" class="btn-link">Purchase Tana</a>
			</p>

		</div>
	</div>
</div>

<script type="text/javascript" src="preview/preview.js"></script>