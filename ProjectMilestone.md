# Seneca Polytechnic

## Group 7 - Project Milestone 1

## Members: - Abby Fernandez

## - Mirac Ozcan

## - Rajini Paranagamage

## Course Name: Advanced Computer Vision

## Course Code: SEA

## Professor: Mana Shahriari

## Date: September 29th, 2025


# Data & Resource Considerations

## Ideas

## - Tracking and Counting Cars in Real-Time Video Feeds (for traffic control and

## management)

## - Computer Vision for Visual / Hearing / Physical Disabilities (for visually impaired

## users, dyslexia, visual question answering, etc.)

## - Tumor Segmentation, Cancer Detection, etc.

## Tracking and Counting Cars in Real-Time Video Feeds (for traffic control and

## management)

## This topic focuses on creating computer vision systems that detect, track, and count vehicles in live video

## streams, supporting applications such as congestion monitoring, adaptive traffic control, and urban

## planning. Real-time performance is essential, requiring algorithms that work under changing conditions

## like weather, occlusion, and camera perspectives. Below are initial thoughts on datasets, tools, and

## possible limitations.

## What datasets might be available?

## A range of open datasets exist for vehicle detection and tracking. The KITTI dataset provides annotated

## stereo videos for urban driving scenes, including detection labels for cars and pedestrians (Geiger et al.,

## 2013). UA-DETRAC contains over 140,000 frames from urban and highway traffic videos with

## annotations for vehicle classes and trajectories, designed for challenging conditions (Wen et al., 2020).

## Cityscapes offers fine-grained semantic segmentation data with 5,000 labeled images from 50 cities,

## useful for dense traffic scenes (Cordts et al., 2016). The BDD100K dataset provides 100,000 videos with

## annotations for objects, lanes, and drivable areas, making it one of the most extensive benchmarks (Yu et

## al., 2020). On Kaggle, datasets such as Vehicle Detection Sample and Output Videos give sample traffic

## footage with YOLO annotations for counting (Kaggle, 2023). City-scale trajectory datasets, like those

## published in Nature, provide millions of anonymized vehicle trajectories from large camera networks

## (Wang et al., 2023). In addition, synthetic data from simulators like CARLA and SUMO can extend

## coverage of rare or extreme scenarios, though with limited realism.

## What datasets might be available?

## A range of open datasets exist for vehicle detection and tracking. The KITTI dataset provides annotated

## stereo videos for urban driving scenes, including detection labels for cars and pedestrians (Geiger et al.,

## 2013). UA-DETRAC contains over 140,000 frames from urban and highway traffic videos with

## annotations for vehicle classes and trajectories, designed for challenging conditions (Wen et al., 2020).

## Cityscapes offers fine-grained semantic segmentation data with 5,000 labeled images from 50 cities,

## useful for dense traffic scenes (Cordts et al., 2016). The BDD100K dataset provides 100,000 videos with

## annotations for objects, lanes, and drivable areas, making it one of the most extensive benchmarks (Yu et

## al., 2020). On Kaggle, datasets such as Vehicle Detection Sample and Output Videos give sample traffic

## footage with YOLO annotations for counting (Kaggle, 2023). City-scale trajectory datasets, like those


#### published in Nature, provide millions of anonymized vehicle trajectories from large camera networks

#### (Wang et al., 2023). In addition, synthetic data from simulators like CARLA and SUMO can extend

#### coverage of rare or extreme scenarios, though with limited realism.

### What tools, libraries, or resources could support your work?

#### OpenCV remains a core library for motion detection, blob analysis, and video processing (Rosebrock,

#### 2019). Deep learning frameworks like PyTorch and TensorFlow support training detection models such as

#### YOLO and multi-object trackers like DeepSORT or ByteTrack (Sergio11, 2021). Ultralytics YOLO is

#### optimized for real-time video analysis. For hardware acceleration, NVIDIA CUDA and TensorRT can

#### reduce latency. Additional resources include Roboflow Universe, which provides pre-trained detection

#### models (Roboflow, 2024), and PyImageSearch tutorials, which show how to integrate detection with

#### speed estimation. On the hardware side, embedded platforms like Raspberry Pi with Hailo AI accelerators

#### enable on-site deployment (Kumar, 2021). Simulation environments such as SUMO can test traffic

#### management strategies virtually. Finally, geospatial integration with tools like ArcGIS APIs allows

#### combining vision-based detection with city traffic planning (FHWA, 2018).

### What limitations might you encounter?

#### Datasets are often biased toward Western urban environments, making it difficult to generalize to traffic in

#### developing countries (Rapid Innovation, 2023). Occlusion in crowded traffic reduces accuracy, especially

#### in overlapping vehicles (Dhruv et al., 2021). Training on massive datasets like BDD100K requires high-

#### end GPUs, while deploying real-time inference on edge devices risks frame drops (AI Accelerator

#### Institute, 2023). Tool integration may lead to version or hardware compatibility problems, particularly

#### when mixing OpenCV with deep learning frameworks. Privacy is a significant issue, as vehicle videos can

#### expose license plates or faces, raising GDPR concerns (ATL Translate, 2023). Dataset licensing can also

#### limit use; for example, KITTI restricts commercial applications. Rare events like accidents are

#### underrepresented in training data, making incident detection unreliable (Authorea, 2023). Finally, ethical

#### risks exist if models perform poorly on non-standard vehicles, leading to bias in traffic enforcement (IRE

#### Journals, 2022). These challenges suggest that resource allocation, anonymization, and balanced

#### dataset collection will be critical for sustainable deployment.

## References

AI Accelerator Institute. (2023). _10 top drivers and challenges in computer vision in 2023_. https://www.aiacceleratorinstitute.com/10-top-drivers-and-challenges-in-computer-
vision-in-2023/
Authorea. (2023). _Real-time vehicle detection and counting for traffic management system_. https://www.authorea.com/users/858543/articles/1242124-real-time-vehicle-
detection-and-counting-for-traffic-management-system
ATL Translate. (2023). _Top 8 problems with computer vision AI_. https://www.atltranslate.com/ai/blog/top- 8 - problems-with-computer-vision-ai
Cordts, M., Omran, M., Ramos, S., Rehfeld, T., Enzweiler, M., Benenson, R., ... & Schiele, B. (2016). The Cityscapes dataset for semantic urban scene understanding.
_Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)_ , 3213–3223.
Dhruv, K., Shashidhar, G., & Yallappa, R. (2021). Vehicle detection and tracking in urban scenarios. _IRE Journals_ , 5(9), 26–33.
https://www.irejournals.com/formatedpaper/1706535.pdf
FHWA. (2018). _Traffic Analysis Toolbox: Volume 1_. U.S. Department of Transportation. https://ops.fhwa.dot.gov/trafficanalysistools/tat_vol1/sect5.htm
Geiger, A., Lenz, P., & Urtasun, R. (2013). Are we ready for autonomous driving? The KITTI vision benchmark suite. _Proceedings of the IEEE Conference on Computer Vision
and Pattern Recognition (CVPR)_ , 3354–3361.
Kaggle. (2023). _Vehicle detection sample and output videos_. https://www.kaggle.com/datasets/vivek603/vehicle-detection-sample-and-output-videos
Kumar, N. B. (2021). _Car detection and tracking system with Raspberry Pi & Hailo AI kit_. Hackster.io. https://www.hackster.io/naveenbskumar/car-detection-and-tracking-
system-with-rpi-hailo-ai-kit-16ef
Rapid Innovation. (2023). _Computer vision for real-time traffic flow analysis_. https://www.rapidinnovation.io/post/computer-vision-for-real-time-traffic-flow-analysis
Roboflow. (2024). _Top object tracking software_. https://blog.roboflow.com/top-object-tracking-software/
Rosebrock, A. (2019). _OpenCV vehicle detection, tracking, and speed estimation_. PyImageSearch. https://pyimagesearch.com/2019/12/02/opencv-vehicle-detection-tracking-
and-speed-estimation/
Sergio11. (2021). _Vehicle detection tracker_. GitHub. https://github.com/sergio11/vehicle_detection_tracker
Wang, Y., Li, X., Zhang, C., & Chen, Y. (2023). City-scale vehicle trajectory dataset. _Scientific Data, 10_ (1), 1589. https://www.nature.com/articles/s41597- 023 - 02589 - y
Wen, L., Du, D., Cai, Z., Lei, Z., Chang, M. C., Qi, H., ... & Lyu, S. (2020). UA-DETRAC: A new benchmark and protocol for multi-object detection and tracking. _Computer Vision
and Image Understanding, 193,_ 102907.
Yu, F., Xian, W., Chen, Y., Liu, F., Liao, M., Madhavan, V., & Darrell, T. (2020). BDD100K: A diverse driving video database. _Proceedings of the IEEE/CVF Conference on
Computer Vision and Pattern Recognition (CVPR)_ , 2636–2645.


### Computer Vision for Visual / Hearing / Physical Disabilities (for visually impaired

### users, dyslexia, visual question answering, etc.)

#### This topic focuses on assistive technologies that leverage computer vision to support individuals with

#### disabilities. Applications include object recognition for visually impaired users, OCR-based text

#### enhancement for dyslexia, sign language translation for hearing impairments, and gesture recognition for

#### physical mobility assistance. A key research area is Visual Question Answering (VQA), which enables

#### interactive systems that can respond to users’ questions about their environments, thus fostering

#### accessibility and independence.

## What datasets might be available?

#### For visually impaired assistance, the VizWiz-VQA dataset is foundational, containing over 30,000 images

#### captured by blind users with real-world questions and annotated answers (Gurari et al., 2018). The VQA

#### dataset provides more than 265,000 images paired with open-ended questions requiring joint vision-

#### language understanding, largely drawn from MS COCO (Antol et al., 2015). OCR-focused datasets, such

#### as ICDAR (International Conference on Document Analysis and Recognition), include annotated natural

#### scene text useful for dyslexia-oriented tools (Karatzas et al., 2015). For physical disabilities, MPII Human

#### Pose provides 25,000 images annotated with body joints for gesture-based recognition (Andriluka et al.,

#### 2014). Datasets like WLASL support hearing-impaired applications by offering large-scale video

#### recordings of sign language gestures (Li et al., 2020). More specialized collections, such as Crucial

#### Object Recognitionfor blind/low-vision navigation, emphasize accessibility-relevant objects (Zhou et al.,

#### 202 3). Many of these datasets are hosted on platforms like Kaggle, VisualQA.org, and VizWiz.org, though

#### some require ethical agreements for use due to the sensitivity of data involving disabled participants

#### (Xiang, 2023).

### What tools, libraries, or resources could support your work?

#### Libraries such as OpenCV enable image preprocessing and feature extraction, while frameworks like

#### PyTorch and TensorFlow support training of multimodal models combining vision and language. For

#### OCR, Tesseract integrates with computer vision workflows to enhance text recognition in natural scenes.

#### Hugging Face Transformers offer pre-trained multimodal models (e.g., BLIP, ViLT) suitable for VQA tasks

#### (Alayrac et al., 2022). Microsoft’s Seeing AI app demonstrates mobile deployment of real-time scene

#### description, while Be My Eyes integrates human and AI vision assistance (Perkins School for the Blind,

#### 2023). In libraries and institutions, FOSS assistive tools like NVDA screen readers, paired with vision-

#### based OCR, provide text-to-speech support (EIFL, 2020). For hearing impairments, sign language

#### recognition systems employ pose-estimation libraries like MediaPipe. On-device platforms such as Edge

#### Impulse allow deploying lightweight AI models to smartphones or embedded devices for real-time

#### support. Training resources include academic guides like the Assistive Technology Guides for Library

#### Patrons from the University of Maryland (UMD CEDI, 2023). Integration with digital libraries and services

#### (e.g., NLS Talking Books, Hoopla, Low Vision Supply devices) demonstrates practical accessibility

#### pipelines (American Academy of Ophthalmology, 2024).

### What limitations might you encounter?

#### The greatest limitation is dataset availability and ethics: studies show that only a small number of

#### accessibility datasets exist compared to broader computer vision fields, often with restricted access due

#### to privacy and consent issues (Hara & Shinohara, 2022). Many datasets exhibit biases, favoring common


#### objects but overlooking context-specific needs of blind or low-vision (BLV) users, causing

#### underperformance in real-world scenarios (Xiang, 2023). For sign language, datasets are often biased

#### toward American Sign Language, limiting generalization to global contexts (Li et al., 2020). Resource

#### constraints include the high data diversity needed to represent the range of disabilities, combined with the

#### cost of specialized hardware like braille displays or wearable cameras (Microsoft Accessibility, 2024).

#### Privacy risks are acute, as real-time visual data may expose sensitive personal environments, raising

#### regulatory concerns under GDPR or HIPAA (ScienceDirect, 2024). Licensing restrictions also limit

#### commercial deployment, datasets like VizWiz explicitly mandate ethical handling and non-commercial use

#### (VizWiz, 2023). Tool compatibility is another issue, as integration with legacy assistive devices may face

#### hardware and software mismatches. Finally, algorithmic bias is a major risk: misinterpretations in sign

#### language translation or OCR could result in exclusionary or even harmful experiences for users (Zhou et

#### al., 2023). These limitations highlight the importance of ethical safeguards, inclusive design, and

#### interdisciplinary collaboration in deploying assistive computer vision.

### References

Alayrac, J. B., Donahue, J., Lucic, M., Clark, A., Tarlow, D., & others. (2022). Flamingo: a visual language model for few-shot learning. _arXiv preprint_.
https://arxiv.org/html/2407.16777v
American Academy of Ophthalmology. (2024). _Low vision impairment: apps and tech assistive devices_. https://www.aao.org/eye-health/tips-prevention/low-vision-impairment-
apps-tech-assistive-devices
Andriluka, M., Pishchulin, L., Gehler, P., & Schiele, B. (2014). 2D human pose estimation: New benchmark and state of the art analysis. _Proceedings of the IEEE Conference on
Computer Vision and Pattern Recognition (CVPR)_ , 3686–3693.
Antol, S., Agrawal, A., Lu, J., Mitchell, M., Batra, D., Lawrence Zitnick, C., & Parikh, D. (2015). VQA: Visual Question Answering. _Proceedings of the IEEE International
Conference on Computer Vision (ICCV)_ , 2425–2433. https://visualqa.org
EIFL. (2020). _FOSS disability tools for libraries: Step-by-step guide_. https://www.eifl.net/resources/foss-disability-tools-libraries-step-step-guide
Gurari, D., Li, Q., Stangl, A. J., Guo, A., Lin, C., Grauman, K., & Luo, J. (2018). VizWiz grand challenge: Answering visual questions from blind people. _Proceedings of the IEEE
Conference on Computer Vision and Pattern Recognition (CVPR)_ , 3608–3617. https://vizwiz.org
Hara, K., & Shinohara, K. (2022). Accessibility dataset gaps and challenges. _ACM Transactions on Accessible Computing, 15_ (4), 1–28.
https://dl.acm.org/doi/fullHtml/10.1145/
Li, D., Rodriguez, C., Yu, X., & Li, H. (2020). Word-level deep sign language recognition from video: A new large-scale dataset and methods comparison. _Proceedings of the
IEEE Winter Conference on Applications of Computer Vision (WACV)_ , 1459–1469.
Microsoft Accessibility. (2024). _Accessibility tools and assistive technology_. https://www.microsoft.com/en-us/accessibility
Perkins School for the Blind. (2023). _Four online services libraries have for low-vision users_. https://www.perkins.org/resource/four-online-services-libraries-have-low-vision-
users-and-everybody-else/
ScienceDirect. (2024). Privacy and ethics in disability datasets. _Social Science & Medicine, 345_ , 115678. https://www.sciencedirect.com/science/article/pii/S
UMD CEDI. (2023). _Assistive technology guides for library patrons with low vision_. Center for the Experience of Disability in Information Access. https://cedi.umd.edu/portfolio-
item/assistive-technology-guides-for-library-patrons-with-low-vision/
VizWiz. (2023). _Tasks and datasets for vision skills_. https://vizwiz.org/tasks-and-datasets/vqa/
Xiang, E. (2023). Being seen versus mis-seen: Disability, AI bias, and misrecognition. _Harvard Journal of Law & Technology, 36_ (1), 1–68.
https://jolt.law.harvard.edu/assets/articlePDFs/v36/Xiang-Being-Seen-Versus-Mis-Seen.pdf
Zhou, T., Chen, W., & Liu, J. (2023). Crucial object recognition for blind navigation. _arXiv preprint_. https://arxiv.org/html/2409.10533v


### Tumor Segmentation, Cancer Detection, etc.

#### This topic focuses on applying medical imaging analysis to identify, classify, and delineate tumors using

#### modalities such as MRI, CT, and X-ray. Such work supports early cancer detection, treatment planning,

#### and patient prognosis. Core tasks include semantic segmentation to map tumor boundaries and

#### classification to distinguish cancer subtypes, often requiring multi-modal datasets and advanced deep

#### learning models.

### What datasets might be available?

#### Prominent datasets include BraTS (Brain Tumor Segmentation) 2020, which provides multi-institutional

#### MRI scans of gliomas, including 369 training cases with labeled tumor sub-regions (Kaggle, 2020). The

#### Medical Segmentation Decathlon contains 10 datasets covering organs and tumors such as the liver and

#### prostate, supporting generalizable segmentation approaches (Medical Decathlon, 2020). The Cancer

#### Imaging Archive (TCIA) hosts collections like UCSF-PDGM for glioblastoma multiforme and multiple other

#### cancers, with de-identified DICOM scans (Clark et al., 2013). On Kaggle, the Brain Tumor MRI Dataset

#### offers 7,023 MRI images categorized into glioma, meningioma, pituitary, and healthy cases (Nickparvar,

#### 2020). The LIDC-IDRI dataset contains over 1,000 CT scans of lung nodules with radiologist annotations

#### (Armato et al., 2011). More recently, AI-generated annotation datasets have been released to

#### complement limited human-labeled data, such as synthetic cancer segmentation labels across 11

#### imaging collections (Zhao et al., 2024). These resources are largely public but typically require ethical

#### approval or signed data use agreements due to patient privacy.

### What tools, libraries, or resources could support your work?

#### Core frameworks include PyTorch and TensorFlow for implementing deep learning models such as U-

#### Net, ResUNet, or transformer-based architectures for segmentation and classification (Ronneberger et

#### al., 2015). Domain-specific libraries like MONAI are tailored to medical imaging, supporting

#### preprocessing, augmentation, and standardized model pipelines (MONAI Consortium, 2020). SimpleITK

#### aids in image registration and DICOM handling. For visualization and prototyping, MATLAB’s Medical

#### Imaging Toolbox provides interactive labeling tools and 3D rendering (MathWorks, 2024). Cloud-based

#### infrastructures such as the NCI Imaging Data Commons co-locate storage with computational tools to

#### enable large-scale analysis (Clark et al., 2022). Open-access repositories like Aylward.org catalog

#### additional imaging datasets and de-identification utilities (Aylward, 2024). Tutorials and benchmarks from

#### Papers With Code accelerate development by comparing state-of-the-art models on metrics like Dice

#### Similarity Coefficient. Supplementary resources include specialized guides (e.g., Milvus tutorials for 3D

#### volume retrieval) and datasets for training generative models that augment tumor data (Nature Machine

#### Intelligence, 2024).

### What limitations might you encounter?

#### Privacy and ethics are major hurdles: while datasets like TCIA are de-identified, risks of re-identification

#### through advanced AI remain (Balthazar et al., 2021). Ethical oversight such as IRB approval is often

#### required. Dataset biasespose challenges, many imaging datasets underrepresent certain ethnic groups or

#### rare tumor types, potentially leading to inequitable model performance (Char et al., 2020). Licensing

#### restrictions may prohibit commercial use of otherwise public datasets. Annotation quality is another issue;

#### segmentation masks may vary across radiologists, introducing noise that reduces model reliability

#### (Isensee et al., 2021). From a technical perspective, 3D medical imaging requires high computational


#### resources, with GPU memory often limiting batch size in volumetric segmentation (Ravi et al., 2023).

#### Noise and artifacts in MRI and CT scans complicate analysis, and cross-institutional variability in

#### scanners introduces interoperability problems (Springer, 2025). While generative AI can augment

#### datasets, poorly validated synthetic data risks degrading model accuracy (Nature, 2024). Finally, funding

#### constraints and lack of standardization across medical imaging protocols slow progress, particularly for

#### generalizable models suitable for clinical deployment (ResearchGate, 2023). These limitations

#### underscore the importance of privacy safeguards, diverse datasets, and rigorous validation before clinical

#### translation.

## References

Armato, S. G., McLennan, G., Bidaut, L., McNitt-Gray, M. F., Meyer, C. R., Reeves, A. P., ... & Clarke, L. P. (2011). The Lung Image Database Consortium (LIDC) and Image
Database Resource Initiative (IDRI): A completed reference database of lung nodules on CT scans. _Medical Physics, 38_ (2), 915–931.
Aylward, S. (2024). _Open-access medical image repositories_. https://www.aylward.org/notes/open-access-medical-image-repositories
Balthazar, P., Harri, P., Prater, A., & Safdar, N. (2021). Ethical and legal considerations in artificial intelligence-driven radiology. _BMC Medical Ethics, 22_ (24), 1–10.
https://bmcmedethics.biomedcentral.com/articles/10.1186/s12910- 021 - 00687 - 3
Char, D. S., Shah, N. H., & Magnus, D. (2020). Implementing machine learning in health care — addressing ethical challenges. _New England Journal of Medicine, 378_ , 981–
983.
Clark, K., Vendt, B., Smith, K., Freymann, J., Kirby, J., Koppel, P., ... & Prior, F. (2013). The Cancer Imaging Archive (TCIA): Maintaining and operating a public information
repository. _Journal of Digital Imaging, 26_ (6), 1045–1057. https://www.cancerimagingarchive.net
Clark, K., et al. (2022). Imaging Data Commons: A cloud-based resource for biomedical imaging. _Scientific Data, 9_ (1), 123. https://datacommons.cancer.gov/repository/imaging-
data-commons
Isensee, F., Jaeger, P. F., Kohl, S. A. A., Petersen, J., & Maier-Hein, K. H. (2021). nnU-Net: a self-adapting framework for biomedical image segmentation. _Nature Methods, 18_ ,
203 – 211.
Kaggle. (2020). _BraTS 2020 training data_. https://www.kaggle.com/datasets/awsaf49/brats2020-training-data
MathWorks. (2024). _Medical Imaging Toolbox_. https://www.mathworks.com/products/medical-imaging.html
Medical Decathlon. (2020). _Medical segmentation decathlon_. [http://medicaldecathlon.com/](http://medicaldecathlon.com/)
MONAI Consortium. (2020). _Medical Open Network for AI (MONAI)_. https://monai.io
Nickparvar, M. (2020). _Brain tumor MRI dataset_. Kaggle. https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset
Ravi, D., Wong, C., Deligianni, F., Berthelot, M., & others. (2023). Challenges in scaling deep learning for 3D medical imaging. _Computer Methods and Programs in
Biomedicine, 235_ , 107512. https://www.sciencedirect.com/science/article/abs/pii/S
Ronneberger, O., Fischer, P., & Brox, T. (2015). U-Net: Convolutional networks for biomedical image segmentation. _Medical Image Computing and Computer-Assisted
Intervention (MICCAI)_ , 234–241.
Springer. (2025). Standardization in AI-based medical imaging: Gaps and recommendations. _AI and Ethics, 7_ , 112–127. https://link.springer.com/article/10.1007/s43681- 025 -
00777 - 7
Zhao, Y., Chen, W., & Li, J. (2024). AI-generated annotations for cancer imaging datasets. _Scientific Data, 11_ (1), 211. https://www.nature.com/articles/s41597- 024 - 03977 - 8


