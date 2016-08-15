node {
    stage 'Checkout'
        checkout scm

    stage 'Build'
        sh 'make build'

    stage 'Archive'
        archive 'build/disk.img'
        archive 'build/tingbot-os.deb'
}