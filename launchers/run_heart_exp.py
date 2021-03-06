from __future__ import print_function
from __future__ import absolute_import
from infogan.misc.distributions import Uniform, Categorical, Gaussian, MeanBernoulli

import tensorflow as tf
import os
from infogan.misc.datasets import HeartDataset
from infogan.models.regularized_gan import RegularizedGAN
from infogan.algos.infogan_trainer import InfoGANTrainer
from infogan.misc.utils import mkdir_p
import dateutil
import dateutil.tz
import datetime

if __name__ == "__main__":

    now = datetime.datetime.now(dateutil.tz.tzlocal())
    timestamp = now.strftime('%Y_%m_%d_%H_%M_%S')

    root_log_dir = "logs/heart"
    root_checkpoint_dir = "ckt/heart"
    batch_size = 256
    updates_per_epoch = 100
    max_epoch = 500

    exp_name = "heart_%s" % timestamp

    log_dir = os.path.join(root_log_dir, exp_name)
    checkpoint_dir = os.path.join(root_checkpoint_dir, exp_name)

    mkdir_p(log_dir)
    mkdir_p(checkpoint_dir)

    #DATASET NEEDS TO GET THE TRAIN SPLIT RIGHT
    #BE CAREFUL OF THIS. NOT TRUE. JUST NEED NEXT BATCH WORKING
    #WHAT DOES INVERSE TRANSFORM DO?
    #SWEET. ALL OF THIS LOOKS GOOD.
    dataset = HeartDataset()


    #THESE DEFINITELY NEED TO BE CHANGED
    #
    # latent_spec = [
    #     (Uniform(62), False),
    #     (Categorical(10), True),
    #     (Uniform(1, fix_std=True), True),
    #     (Uniform(1, fix_std=True), True),
    # ]
    #SAME LATENT SPEC AS REPORTED FOR FACES
    latent_spec = [
        (Uniform(128), False),
        (Uniform(1, fix_std=True), True),
        (Uniform(1, fix_std=True), True),
        (Uniform(1, fix_std=True), True),
        (Uniform(1, fix_std=True), True),
        (Uniform(1, fix_std=True), True)
    ]

    #EVERYTHING SEEMS FINE. NETWORK ARCHITECTURE SHOULD
    #BE CHANGED.
    model = RegularizedGAN(
        output_dist=MeanBernoulli(dataset.image_dim),
        latent_spec=latent_spec,
        batch_size=batch_size,
        image_shape=dataset.image_shape,
        network_type="heart",
    )

    #EVERYTHING SEEMS OKAY HERE
    #JUST NEED TO MAKE SURE NEXT_BATCH
    #IS READY TO GO
    #LEARNING RATES MIGHT NEED TO CHANGE
    algo = InfoGANTrainer(
        model=model,
        dataset=dataset,
        batch_size=batch_size,
        exp_name=exp_name,
        log_dir=log_dir,
        checkpoint_dir=checkpoint_dir,
        max_epoch=max_epoch,
        updates_per_epoch=updates_per_epoch,
        info_reg_coeff=0.1,#1.0, RECAPUTULATE AZIMUTH FACE TEST
        generator_learning_rate=5e-4,#1e-3,
        discriminator_learning_rate=2e-4#2e-4,
    )

    algo.train()
