cd ..
FILE_PATH=$1
HEATMAP_PATH="heat.png"
python run_covidnet_ct.py infer --model_dir models/COVID-Net_CT-2_L --meta_name model.meta --ckpt_name model --image_file $FILE_PATH --heatmap --heatmap_dir $HEATMAP_PATH


